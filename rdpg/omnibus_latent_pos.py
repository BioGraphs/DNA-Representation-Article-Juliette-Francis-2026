"""omnibus_latent_pos

This script creates an omnibus matrix for every pair of embeddings 
in the input list. It generates binary data kernels from the embeddings 
using k-nearest neighbors, constructs an omnibus matrix from each pair, 
and then applies **Adjacency Spectral Embedding (ASE)** to extract 
latent positions for both inputs. The resulting latent positions are 
stored in HDF5 (`.h5`) files for each embedding pair.
Each HDF5 file contains:
- `'emb1'`: Latent position matrix of the first embedding in the pair.
- `'emb2'`: Latent position matrix of the second embedding in the pair.

Arguments:
-----------
- `embedding_list` (str): Comma-separated list of paths to embedding CSV 
                          files. Example: `emb1.csv,emb2.csv,emb3.csv`.
- `k` (int): Number of neighbors used to compute the data kernel.
- `output_dir` (str): Directory where the resulting `.h5` files will be saved.
- `distance` (str): Distance metric for the k-nearest neighbors (`euclidean` or `cosine`).
- `dimensions` (int): Desired dimensionality of the ASE output.
- `knn_method` (str): Wether to do KNN or mutual KNN for the graph construction (`KNN` or `MKNN`).
- `--memory_light` (-m, bool): Whether to use a lightweight version of RDPG (default: False).
"""
import numpy as np
import h5py
import os
import scipy
from graspologic.embed import AdjacencySpectralEmbed
import time
import argparse
import warnings
from numpy import genfromtxt
import gc
# warnings.filterwarnings('ignore')
from data_kernel_latent_pos import data_kernel


def create_ase_omnibus_matrix(A1, A2, n_components, save_memory):
    """
    Constructs an omnibus matrix of A1 and A2, then computes adjacency 
    spectral embedding of the resulting omnibus matrix to create latent 
    positions matrices of A1 and A2 aligned.

    Parameters
    ----------
    A1, A2: ndarray of shape (n_samples, n_samples)
        Data kernel corresponding to the adjacency matrix symmetrized.
    n_components: int
        The number of components of the ASE
    save_memory: bool
        Wether to do the lighter memory method or not.

    Returns
    -------
    z_omnibus 1, z_omnibus 2: ndarray of shape (n_samples, n_components)
        Latent positions matrices of A1 and A2 aligned.
    """
    corner = (A1 + A2) / 2
    omnibus_matrix = np.block([[A1, corner], [corner, A2]])
    if save_memory:
        U, D, V = scipy.sparse.linalg.svds(omnibus_matrix, k=n_components)
        del omnibus_matrix
        gc.collect()
        idx = np.argsort(D)[::-1]
        D = D[idx]
        U = U[:, idx]
        z_omnibus = U @ np.diag(np.sqrt(D))
        return z_omnibus[:A1.shape[0]], z_omnibus[A1.shape[0]:]
    ase = AdjacencySpectralEmbed(n_components=n_components, algorithm='truncated', check_lcc=False, diag_aug=False)
    z_omnibus = ase.fit_transform(omnibus_matrix)
    return z_omnibus[:A1.shape[0]], z_omnibus[A1.shape[0]:]


def main(embedding_list, k, output_dir, distance, dimensions, knn_method, save_memory=False):
    for emb1_file in embedding_list:
        emb1_name = os.path.splitext(os.path.basename(emb1_file))[0]
        emb1 = np.genfromtxt(emb1_file, delimiter=',')[:, 2:]
        A1 = data_kernel(emb1, k, distance, knn_method)

        if dimensions == 0:
            ase_tmp = AdjacencySpectralEmbed(algorithm='truncated', check_lcc=False, diag_aug=False)
            Z_tmp = ase_tmp.fit_transform(A1)
            d = Z_tmp.shape[1]
        else:
            d = dimensions

        for emb2_file in embedding_list:
            emb2_name = os.path.splitext(os.path.basename(emb2_file))[0]
            if emb1_name == emb2_name:
                continue
            emb2 = genfromtxt(emb2_file, delimiter=',')[:, 2:]
            A2 = data_kernel(emb2, k, distance, knn_method)

            start_time = time.time()
            Z1, Z2 = create_ase_omnibus_matrix(A1, A2, d, save_memory)
            end_time = time.time()
            print(f"ASE running time for {emb1_name} and {emb2_name} omnibus matrix: ", end_time - start_time)
            output_file = f"{output_dir}/{emb1_name}_{emb2_name}_{distance}_{knn_method}_k-{k}_d-{dimensions}_omnibus_latent_position.h5"
            with h5py.File(output_file, 'w') as f:
                f.create_dataset('emb1', data=Z1)
                f.create_dataset('emb2', data=Z2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='Create latent position matrix from the omnibus matrix of 2 embeddings')
    parser.add_argument(
                'embedding_list',
                type=lambda s: [str(item) for item in s.split(',')],
                help="The list of embeddings")
    parser.add_argument(
                'k',
                type=int,
                help="The number of neighbors for data kernels")
    parser.add_argument(
                'output_dir',
                type=str,
                help="The results directory")
    parser.add_argument(
                'distance',
                type=str,
                help="The metric distance used to calculate the data kernel")
    parser.add_argument(
                'dimensions',
                type=int,
                help="Desired dimensionality for the omnibus spectral embeddings")
    parser.add_argument('knn_method',
                type=str,
                choices=['KNN', 'MKNN'],
                help="Wether to do KNN or mutual KNN for the graph construction")
    parser.add_argument(
                '-m', '--memory_light',
                action='store_true',
                help="Whether to use the lighter version of the RPDG model")
    args = parser.parse_args()
    main(args.embedding_list, args.k, args.output_dir, args.distance, args.dimensions, args.knn_method, args.memory_light)
