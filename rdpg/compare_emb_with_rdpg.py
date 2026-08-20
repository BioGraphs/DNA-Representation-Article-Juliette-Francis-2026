"""compare_emb_with_rdpg

Compares two graph embeddings using a Random Dot Product Graph (RDPG) framework.
It is designed to evaluate the similarity between two sets of graph embeddings by computing
Z distances between matched points in the joint (omnibus) embedding space and comparing
these distances to a null distribution derived under the null hypothesis (H0) of no structural
difference between the graphs.
The script outputs summary statistics of the p-values (mean, median, quantiles, etc.) and 
writes them to a JSON file.

Arguments:
- `latent_pos` (str): Path to the CSV file containing the latent positions of the first graph embedding.
- `omnibus_latent_pos` (str): Path to the HDF5 (.h5) file containing the omnibus latent positions. 
- `h0_z_distance` (str): Path to the JSON file containing the null distribution of Z distances 
                         and associated p-values computed under H0.
- `output_file` (str): Path where the output JSON file with results will be saved.
"""

import numpy as np
from numpy import genfromtxt
import statistics
import json
import time
import argparse
import os
import warnings
import h5py
from create_h0_distributions import compute_p_values
# warnings.filterwarnings('ignore')


def main(latent_pos_path, omnibus_path, h0_z_distance_path, output_file):
    Z1 = genfromtxt(latent_pos_path, delimiter=',')
    
    with open(h0_z_distance_path) as json_file:
        h0_distribution = json.load(json_file)
    h0_z_distance = h0_distribution['H0 Z distances']

    with h5py.File(omnibus_path, 'r') as f:
        Z1_omni = f['emb1'][:]
        Z2_omni = f['emb2'][:]
    z_distance = np.linalg.norm(Z1_omni - Z2_omni, axis=1)
    p_values = compute_p_values(z_distance, h0_z_distance)

    z_distance_list = z_distance.tolist()
    p_values_list = p_values.tolist() if isinstance(p_values, np.ndarray) else list(p_values)
    results = {
        'Mean p-value': float(statistics.mean(p_values)), 
        'Median p-value': float(statistics.median(p_values)), 
        'Minimum p-value': float(min(p_values)),
        'Maximum p-value': float(max(p_values)),
        'Quantiles': [float(q) for q in statistics.quantiles(p_values)],
        'p-values': p_values_list,
        'Z distance': z_distance_list,
        'd': Z1.shape[1]
    }
    with open(output_file, "w") as outfile:
        json.dump(results, outfile, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='Compare embeddings with RDPG')
    parser.add_argument('latent_pos',
                            type=str,
                            help="The latent positions matrix of the first embedding")
    parser.add_argument('omnibus_latent_pos',
                            type=str,
                            help="The latent positions matrix of the omnibus of the two embeddings")
    parser.add_argument('h0_z_distance',
                            type=str,
                            help="The null distribution of latent positions distances")
    parser.add_argument('output_file',
                            type=str,
                            help="The output file path")
    args = parser.parse_args()
    main(args.latent_pos, args.omnibus_latent_pos, args.h0_z_distance, args.output_file) 
