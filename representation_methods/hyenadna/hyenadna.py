import json
import os
import csv
import numpy as np
import pandas as pd
import argparse
import torch
import re
import time
import subprocess
from transformers import PreTrainedModel
import importlib
hyena_dna = importlib.import_module("hyena-dna.standalone_hyenadna")
CharacterTokenizer = hyena_dna.CharacterTokenizer
HyenaDNAModel = hyena_dna.HyenaDNAModel


######################### HyenaDNA part #########################
# helper 1
def inject_substring(orig_str):
    """Hack to handle matching keys between models trained with and without
    gradient checkpointing."""

    # modify for mixer keys
    pattern = r"\.mixer"
    injection = ".mixer.layer"

    modified_string = re.sub(pattern, injection, orig_str)

    # modify for mlp keys
    pattern = r"\.mlp"
    injection = ".mlp.layer"

    modified_string = re.sub(pattern, injection, modified_string)

    return modified_string


# helper 2
def load_weights(scratch_dict, pretrained_dict, checkpointing=False):
    """Loads pretrained (backbone only) weights into the scratch state dict."""

    # loop thru state dict of scratch
    # find the corresponding weights in the loaded model, and set it

    # need to do some state dict "surgery"
    for key, value in scratch_dict.items():
        if 'backbone' in key:
            # the state dicts differ by one prefix, '.model', so we add that
            key_loaded = 'model.' + key
            # breakpoint()
            # need to add an extra ".layer" in key
            if checkpointing:
                key_loaded = inject_substring(key_loaded)
            try:
                scratch_dict[key] = pretrained_dict[key_loaded]
            except:
                raise Exception('key mismatch in the state dicts!')

    # scratch_dict has been updated
    return scratch_dict


class HyenaDNAPreTrainedModel(PreTrainedModel):
    """
    An abstract class to handle weights initialization and a simple interface for downloading and loading pretrained
    models.
    """
    base_model_prefix = "hyenadna"

    def __init__(self, config):
        pass

    def forward(self, input_ids, **kwargs):
        return self.model(input_ids, **kwargs)

    @classmethod
    def from_pretrained(cls,
                        path,
                        model_name,
                        download=False,
                        config=None,
                        device='cpu',
                        use_head=False,
                        n_classes=2,
                      ):
        # first check if it is a local path
        pretrained_model_name_or_path = os.path.join(path, model_name)
        if os.path.isdir(pretrained_model_name_or_path) and download == False:
            if config is None:
                config = json.load(open(os.path.join(pretrained_model_name_or_path, 'config.json')))
        else:
            hf_url = f'https://huggingface.co/LongSafari/{model_name}'

            subprocess.run(f'rm -rf {pretrained_model_name_or_path}', shell=True)
            command = f'mkdir -p {path} && cd {path} && git lfs install && git clone {hf_url}'
            subprocess.run(command, shell=True)

            if config is None:
                config = json.load(open(os.path.join(pretrained_model_name_or_path, 'config.json')))

        scratch_model = HyenaDNAModel(**config, use_head=use_head, n_classes=n_classes)  # the new model format
        loaded_ckpt = torch.load(
            os.path.join(pretrained_model_name_or_path, 'weights.ckpt'),
            map_location=torch.device(device)
        )

        # need to load weights slightly different if using gradient checkpointing
        if config.get("checkpoint_mixer", False):
            checkpointing = config["checkpoint_mixer"] == True or config["checkpoint_mixer"] == True
        else:
            checkpointing = False

        # grab state dict from both and load weights
        state_dict = load_weights(scratch_model.state_dict(), loaded_ckpt['state_dict'], checkpointing=checkpointing)

        # scratch model has now been updated
        scratch_model.load_state_dict(state_dict)
        print("Loaded pretrained weights ok!")
        return scratch_model
#################################################################


def main(input_file, output_file):
    if os.path.isfile(output_file):
        raise ValueError(f"Output file '{output_file}' already exists. Please delete the existing file if you want to use this name")

    # Load DNA sequences file___________________________________________
    dna_seq_list = []
    species_list = []
    with open(input_file) as fd:
        rd = csv.reader(fd, delimiter=",", quotechar='"')
        first_row = True
        for row in rd:
            if first_row:
                first_row = False
                continue
            dna_seq_list.append(row[0])
            species_list.append(row[1])

    # Load the model from huggingface___________________________________
    pretrained_model_name = 'hyenadna-small-32k-seqlen'
    max_length = 32768 

    # data settings:
    use_padding = True
    rc_aug = False  # reverse complement augmentation
    add_eos = False  # add end of sentence token
    # we need these for the decoder head, if using
    use_head = False
    n_classes = 2  # not used for embeddings only
    # you can override with your own backbone config here if you want,
    # otherwise we'll load the HF one in None
    backbone_cfg = None

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = HyenaDNAPreTrainedModel.from_pretrained(
            '/hyenadna',
            pretrained_model_name,
            download=False,
            config=backbone_cfg,
            device=device,
            use_head=use_head,
            n_classes=n_classes)
    tokenizer = CharacterTokenizer(
        characters=['A', 'C', 'G', 'T', 'N'],  # add DNA characters, N is uncertain
        model_max_length=max_length + 2,  # to account for special tokens, like EOS
        add_special_tokens=False,  # we handle special tokens elsewhere
        padding_side='left') # since HyenaDNA is causal, we pad on the left

    # Calculate the embedding of dna sequences__________________________
    start_time = time.time()
    for i in range(len(dna_seq_list)):
        tok_seq = tokenizer(dna_seq_list[i])
        tok_seq = tok_seq["input_ids"]  # grab ids
        # place on device, convert to tensor
        tok_seq = torch.LongTensor(tok_seq).unsqueeze(0)  # unsqueeze for batch dim
        tok_seq = tok_seq.to(device)
        # prep model and forward
        model.to(device)
        model.eval()
        with torch.inference_mode():
            embeddings = model(tok_seq)
        embedding_mean = torch.mean(embeddings[0], dim=0) 
        embedding_mean_np = embedding_mean.detach().cpu().numpy()
        embedding_columns = [f"embedding_{j}" for j in range(embedding_mean_np.shape[0])]
        embedding_df = pd.DataFrame([embedding_mean_np], columns=embedding_columns)
        row = {'dna_seq': dna_seq_list[i],
               'species': species_list[i]}
        row_df = pd.DataFrame([row])
        df = pd.concat([row_df, embedding_df], axis=1)
        df.to_csv(output_file, mode='a', header=False, index=False)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"Running time: {running_time} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='HyenaDNA embedding',
                            description=("HyenaDNA is a foundation model designed for generating DNA embedding."))
    parser.add_argument('input_file',
                            type=str,
                            help="The DNA sequences file")
    parser.add_argument('output_file',
                            type=str,
                            help="The DNA sequences embeddings file") 
    args = parser.parse_args()
    main(args.input_file, args.output_file)