import torch
from transformers import AutoTokenizer, AutoModel
from transformers.models.bert.configuration_bert import BertConfig
import csv
import numpy as np
import pandas as pd
import argparse
import time
import os

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
	''' class transformers.AutoTokenizer
	This is a generic tokenizer class that will be instantiated as one 
	of the tokenizer classes of the library when created with the 
	AutoTokenizer.from_pretrained() class method.
	AutoTokenizer.from_pretrained instantiates one of the tokenizer 
	classes of the library from a pretrained model vocabulary
	'''
	tokenizer = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
	''' class transformers.BertConfig
	This is a model configuration class with all the parameters of 
	the model. The from_pretrained() method is used to load 
	the model weights.
	'''
	config = BertConfig.from_pretrained("zhihan1996/DNABERT-2-117M")
	''' class transformers.AutoModel
	This is a generic model class that will be instantiated as one 
	of the base model classes of the library when created with the 
	from_pretrained() class method or the from_config() class method.
	'''
	model = AutoModel.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True, config=config)

	# Calculate the embedding of dna sequences__________________________

	'''tokenizer
	return_tensors (str or TensorType, optional) -> If set, will return 
	tensors instead of list of python integers. 
	'pt': Return PyTorch torch.Tensor objects
	padding=True -> When inputs have different lengths, they can’t be 
	converted to fixed-size tensors. For dealing with this problem,  
	padding adds a special padding token to ensure sequences will have 
	the same length (as the longest sequence).

	tokens is constituted of 3 tensors : 
	- input_ids : List of token ids to be fed to a model
	- token_type_ids : List of token type ids to be fed to a model. 
	It seems to be used when models’ purpose is to do classification on 
	pairs of sentences or question answering
	- attention_mask : List of indices specifying which tokens should 
	be attended to by the model
	'''
	tokens = tokenizer(dna_seq_list, return_tensors = 'pt', padding=True)
	inputs = tokens["input_ids"]
	device = 'cuda' if torch.cuda.is_available() else 'cpu'
	model = model.to(device)
	inputs = inputs.to(device)
	start_time = time.time()
	for i in range(len(dna_seq_list)):
		input_token = inputs[i].reshape(1, inputs[i].shape[0])
		print(input_token.shape)
		print(input_token)
		model_output = model(input_token)
		# model_output is constituted of 2 tensors :
		# - hidden_states (model_output[0]) : Sequence of hidden-states 
		# at the output of the last layer of the model.
		# model_output[0].shape -> [1, inputs[i].shape[0], 768]
		# Each token (inputs[i].shape[0] tokens) is embedded
		# - pooler_output (model_output[1]) : Last layer hidden-state of 
		# the first token of the sequence (classification token) further 
		# processed by a Linear layer and a Tanh activation function. 
		# model_output[1].shape -> [1, 768]
		hidden_states = model_output[0]
		# embedding with mean pooling
		embedding_mean = torch.mean(hidden_states[0], dim=0)
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
	                        prog='DNABERT2 embedding',
	                        description=("DNABERT2 is a foundation model designed for generating DNA embedding."))
	parser.add_argument('input_file',
	                        type=str,
	                        help="The DNA sequences file")
	parser.add_argument('output_file',
	                        type=str,
	                        help="The DNA sequences embeddings file") 
	args = parser.parse_args()
	main(args.input_file, args.output_file)