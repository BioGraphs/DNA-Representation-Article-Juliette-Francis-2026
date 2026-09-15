from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
import pandas as pd 
import argparse
import time
import os
from itertools import product

def which_vocabulary(k):
    '''
    Creates list of all possible k-mers
    '''
    kmers = list(product('ATGC', repeat=k))
    vocabulary = [''.join(kmer) for kmer in kmers]
    return vocabulary

def extract_kmers(sequence, k):
    '''
    Creates list of k-mers from a sequence
    '''
    if k == 1:
    	return list(sequence)
    else:
        return [sequence[i:i+k] for i in range(len(sequence) - k + 1)]

def TNF_with_frequencies(sequences, k, vocabulary):
    '''
    Returns a matrix where each row corresponds to the frequency 
    of every possible k-mer and a vector containing each k-mers
    '''
    kmers_list = [' '.join(extract_kmers(seq, k)) for seq in sequences]
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), lowercase=False, vocabulary=vocabulary)
    X = vectorizer.fit_transform(kmers_list)
    kmers_matrix = X.toarray()
    return kmers_matrix, vectorizer.get_feature_names_out()


def TNF_with_relative_frequencies(sequences, k, vocabulary):
    '''
    Returns a matrix where each row corresponds to the relative frequency 
    of every possible k-mer and a vector containing each k-mers
    '''
    kmers_list = [' '.join(extract_kmers(seq, k)) for seq in sequences]
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), lowercase=False, vocabulary=vocabulary)
    X = vectorizer.fit_transform(kmers_list)
    kmers_matrix = X.toarray()
    relative_frequencies = []
    for row in kmers_matrix:
        total_kmers = sum(row)
        relative_frequencies.append(row / total_kmers if total_kmers > 0 else row)
    return np.array(relative_frequencies), vectorizer.get_feature_names_out()


def main(input_file, output_file, k):
    vocabulary = which_vocabulary(k)

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

    # Calculate the embedding of dna sequences__________________________
    start_time = time.time()
    relative_frequencies, vocabulary = TNF_with_relative_frequencies(dna_seq_list, k, vocabulary)
    embeddings_np = np.array(relative_frequencies)

    embedding_df = pd.DataFrame(embeddings_np)
    row = {'dna_seq': dna_seq_list,
           'species': species_list}
    row_df = pd.DataFrame(row)
    df = pd.concat([row_df, embedding_df], axis=1)
    df.to_csv(output_file, mode='a', header=False, index=False)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"Running time: {running_time} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='Bag-of-k-mers embedding',
                            description=("TNF is a method that calculates k-mers frequencies, which can be used as DNA embedding."))
    parser.add_argument('input_file',
                            type=str,
                            help="The DNA sequences file")
    parser.add_argument('output_file',
                            type=str,
                            help="The DNA sequences embeddings file")
    parser.add_argument('k',
                            type=int,
                            help="The k-mers size")
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.k)