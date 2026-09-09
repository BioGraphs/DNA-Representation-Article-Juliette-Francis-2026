"""create_h0_distribution

It creates null distributions of distances using simulated graphs from a latent position matrix via 
RDPG (Random Dot Product Graph). The distribution is made with latent position distances between pairs 
of omnibus matrices. It also Creates a null distribution of p-values to statistically evaluate differences 
between embeddings. It optionally supports a memory-efficient mode using a lighter graph simulation.

Arguments:
-----------
- `embedding` (str): Path to the original embedding CSV file.
- `latent_pos` (str): Path to the CSV file of latent positions.

- `k` (int): Number of neighbors used to compute the data kernel.
- `n` (int): Number of bootstrap samples to generate the null distribution.
- `output_dir` (str): Directory where the resulting `.h5` files will be saved.
- `distance` (str): Distance metric for the k-nearest neighbors (`euclidean` or `cosine`).
- `output_file_z` (str): Path to save H0 latent positions matrices.
- `knn_method` (str): Wether to do KNN or mutual KNN for the graph construction (`KNN` or `MKNN`).
- `--memory_light` (-m, bool): Whether to use a lightweight version of RDPG (default: False).
"""
import numpy as np
import pandas as pd
from numpy import genfromtxt
from graspologic.simulations import rdpg
import statistics
import json
import time
import argparse
import os
import warnings
import h5py
import gc
from data_kernel_latent_pos import data_kernel
from omnibus_latent_pos import create_ase_omnibus_matrix


def rdpg_light(Z):
    """
    Samples a random graph based on the latent positions in Z.
    This function is an lighter memory alternative to the Graspologic
    graspologic.simulations.rdpg function.

    Parameters
    ----------
    Z: ndarray of shape (n_samples, n_components)
        Latent positions of a symmetric graph

    Returns
    -------
    A: ndarray of shape (n_samples, n_samples)
        Adjacency matrix of a random graph sampled from the 
        RDPG made with Z
    """
    n = Z.shape[0]
    P = Z @ Z.T
    np.fill_diagonal(P, 0)
    np.clip(P, 0, 1, out=P)
    triu_indices = np.triu_indices(n, k=1)
    upper_vals = np.random.binomial(1, P[triu_indices])
    A = np.zeros((n, n), dtype=np.uint8)
    A[triu_indices] = upper_vals
    A += A.T
    return A


def compute_p_values(z_distance, h0_z_distances):
    """
    Calculates p-values associated to each observed distance of 
    z_distance from the null distribution h0_z_distances. The p-value 
    is calculated by subtracting the percentile at which the observed 
    distance falls in the null distribution from 1.

    Parameters
    ----------
    z_distance: ndarray of shape (n_samples,)
        The euclidean norms between two latent positions matices
        Z1 and Z2 (np.linalg.norm(Z1 - Z2), axis=1)
    h0_z_distances: list of length n_boostraps
        The null distribution of euclidean norms between Z1 and 
        a latent position Z1_prime made from Z1 and its RDPG. 

    Returns
    -------
    p_values: list of floats (length = n_samples)
        The list of p-values associated to each observed distance of 
        z_distance 
    """
    h0_z = np.array(h0_z_distances + [z_distance])
    p_values = []
    i = 0
    for row in h0_z.T:
        p_values.append(1 - (sum(z_distance[i] > row) / len(row)))
        i += 1
    return p_values


def get_h0_z_distances(A, Z, n_boostraps, save_memory, output_file_z):
    """
    Calculates the null distribution of euclidean norms between Z and 
    a latent position Z_prime made from Z and its RDPG.

    Parameters
    ----------
    A: ndarray of shape (n_samples, n_samples)
        Data kernel corresponding to a adjacency matrix symmetrized.
    Z: ndarray of shape (n_samples, n_components)
        Latent positions of A
    n_boostraps: int
        Number of bootstraps for the null distribution
    save_memory: bool
        Wether to do the lighter memory method or not.
    output_file_z: str
        Path to save H0 latent positions matrices.

    Returns
    -------
    h0_z_distances: list of length n_boostraps
        The null distribution of euclidean norms. 
    """
    h0_z_distances = []
    if save_memory:
        for i in range(n_boostraps):
            A_prime = rdpg_light(Z)
            Z_omni, Z_omni_prime = create_ase_omnibus_matrix(A, A_prime, Z.shape[1], save_memory)
            del A_prime
            h0_z_distances.append(np.linalg.norm(Z_omni - Z_omni_prime, axis=1))
            del Z_omni
            del Z_omni_prime
            del columns
            del df_omni
            del df_omni_prime
            del df_combined
            gc.collect()
        return h0_z_distances

    for i in range(n_boostraps):
        A_prime = rdpg(Z,
          loops=False,
          rescale=False,
          directed=False) 
        Z_omni, Z_omni_prime = create_ase_omnibus_matrix(A, A_prime, Z.shape[1], save_memory)
        h0_z_distances.append(np.linalg.norm(Z_omni - Z_omni_prime, axis=1))
    return h0_z_distances


def main(embedding_path, latent_pos_path, k, n_boostraps, save_memory, output_file, distance, output_file_z, knn_method):
    emb = np.genfromtxt(embedding_path, delimiter=',')[:, 2:]
    A = data_kernel(emb, k, distance, knn_method)
    Z = genfromtxt(latent_pos_path, delimiter=',')
    h0_z_distances = get_h0_z_distances(A, Z, n_boostraps, save_memory, output_file_z)
    h0_distributions = {
        'H0 Z distances': [[float(value) for value in sublist] for sublist in h0_z_distances],
        'Number of bootstraps': n_boostraps + 1,
        'Saving memory': save_memory,
        'd': Z.shape[1]
    }
    with open(output_file, "w") as outfile:
        json.dump(h0_distributions, outfile, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='')
    parser.add_argument('embedding',
                            type=str,
                            help="The embedding")
    parser.add_argument('latent_pos',
                            type=str,
                            help="The latent positions matrix of the first embedding")
    parser.add_argument('k',
                            type=int,
                            help="The number of neighbors for data kernels")
    parser.add_argument('n',
                            type=int,
                            help="Number of bootstraps for the null distribution")
    parser.add_argument('output_file',
                            type=str,
                            help="The output file path")
    parser.add_argument('distance',
                            type=str,
                            help="The metric distance used to calculate the data kernel")
    parser.add_argument('output_file_z',
                            type=str,
                            help="The output file of H0 latent positions path")
    parser.add_argument('knn_method',
                            type=str,
                            choices=['KNN', 'MKNN'],
                            help="Wether to do KNN or mutual KNN for the graph construction")
    parser.add_argument('-m', '--memory_light', 
                            action='store_true',
                            help="Whether to use the lighter version of the RPDG model")
    args = parser.parse_args()
    main(args.embedding, 
        args.latent_pos, 
        args.k, 
        args.n, 
        args.memory_light, 
        args.output_file, 
        args.distance, 
        args.output_file_z, 
        args.knn_method)
