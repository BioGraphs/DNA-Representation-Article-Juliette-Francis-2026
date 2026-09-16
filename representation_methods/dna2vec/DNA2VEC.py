import os
from dna2vec.dna2vec.multi_k_model import MultiKModel
import numpy as np
import csv
import pandas as pd
import argparse
import time

def extract_kmers(sequence, k):
    '''
    Creates list of k-mers from a sequence
    '''
    if k == 1:
        return list(sequence)
    else:
        return [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
        

def main(input_file, output_file, k, weights_path):
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

    # Load the model ___________________________________________________
    mk_model = MultiKModel(weights_path)

    # Calculate the embedding of dna sequences__________________________
    start_time = time.time()
    for i in range(len(dna_seq_list)):
        sequence_4mers = extract_kmers(dna_seq_list[i], k)
        vec_list = []
        for j in range(len(sequence_4mers)):
            # fetch vectors representations
            vec_list.append(mk_model.vector(sequence_4mers[j]))
        vec_array = np.stack(vec_list, axis=0)
        # embedding with mean pooling
        embedding_mean_np = np.mean(vec_array, axis=0)

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
                            prog='Dna2vec embedding',
                            description=("Dna2vec is an open-source library to train distributed representations of variable-length k-mers."))
    parser.add_argument('input_file',
                            type=str,
                            help="The DNA sequences file")
    parser.add_argument('output_file',
                            type=str,
                            help="The DNA sequences embeddings file")
    parser.add_argument('k',
                            type=int,
                            help="The k-mers size")
    parser.add_argument('weights',
                            type=str,
                            help="The path to the dna2vec model weights")
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.k, args.weights)
