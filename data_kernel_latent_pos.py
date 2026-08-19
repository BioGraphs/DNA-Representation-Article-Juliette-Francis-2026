"""data_kernel_latent_pos

This script generates a binary data kernel (adjacency-like matrix) 
from a given embedding using a specified distance metric and the k-nearest 
neighbors algorithm. It then applies Adjacency Spectral Embedding (ASE) 
to compute a low-dimensional latent position matrix from the resulting graph 
structure. The outputs are saved as CSV files.

Arguments:
-----------
- `embedding` (str): Path to the input embedding file (CSV format). The script 
                     assumes the actual features start from the third column.
- `distance` (str): Distance metric for the k-nearest neighbors (`euclidean` or `cosine`).
- `k` (int): Number of neighbors used to construct the data kernel.
- `output_name` (str): Base name and path used for output files.
- `dimensions` (int): Desired dimensionality of the ASE output.
- `knn_method` (str): Wether to do KNN or mutual KNN for the graph construction (`KNN` or `MKNN`).

Outputs:
---------
- A CSV file containing the latent positions with specified dimensionality: 
    `<output_name>_d-<dimensions>_latent_position.csv`
"""
import numpy as np
from graspologic.embed import AdjacencySpectralEmbed
import sklearn.neighbors as neighbors
import time
import torch
import argparse
import warnings
warnings.filterwarnings('ignore')


def data_kernel(Y, k, dist='euclidean', knn_method='KNN'):
    """
    Constructs a data kernel corresponding to the adjacency matrix of a 
    k-nearest neighbors graph symmetrized. The k-nearest neighbors can
    be determine with the euclidean distance or the cosine distance.

    Parameters
    ----------
    Y: ndarray of shape (n_samples, n_features)
        Data matrix where each row corresponds to a data point in feature space.

    k: int
        The number of nearest neighbors to consider for each data point.

    dist: str, optional (default='euclidean')
        The distance or similarity metric to use:
        - 'euclidean': Uses Euclidean distance to find neighbors.
        - 'cosine'  : Uses cosine similarity (via dot product).

    knn_method: str, optional (default='KNN')
        Wether to do KNN or mutual KNN for the graph construction:
        - 'KNN': Uses k-nearest neighbors algorithm
        - 'MKNN' Uses mutual k-nearest neighbors algorithm

    Returns
    -------
    data_kernel: ndarray of shape (n_samples, n_samples)
        A binary matrix where entry (i, j) is 1 if sample j is among the k-nearest 
        neighbors of sample i or if sample i is among the k nearest neighbors
        of sample j, and 0 otherwise.
    """
    if dist == 'euclidean' and knn_method == 'KNN':
        neigh = neighbors.NearestNeighbors(n_neighbors=k, metric='euclidean')
        neigh.fit(Y)
        neighbors_ind = neigh.kneighbors(return_distance=False)
        data_kernel = np.zeros((Y.shape[0],Y.shape[0]), dtype=np.uint8)
        for i in range(Y.shape[0]):
            data_kernel[i, neighbors_ind[i]] = 1
            data_kernel[neighbors_ind[i], i] = 1
        return data_kernel
    elif dist == 'euclidean' and knn_method == 'MKNN':
        neigh = neighbors.NearestNeighbors(n_neighbors=k, metric='euclidean')
        neigh.fit(Y)
        neighbors_ind = neigh.kneighbors(return_distance=False)
        data_kernel = np.zeros((Y.shape[0], Y.shape[0]), dtype=np.uint8)
        for i in range(Y.shape[0]):
            data_kernel[i, neighbors_ind[i]] = 1
        data_kernel = np.logical_and(data_kernel, data_kernel.T).astype(np.uint8)
        return data_kernel
    elif dist == 'cosine' and knn_method == 'KNN':
        Y_Yt = torch.from_numpy(Y @ Y.T)
        mask = torch.eye(Y_Yt.shape[0], dtype=bool)
        Y_Yt[mask] = -float('inf')
        data_kernel = torch.zeros_like(Y_Yt)
        _, top_k_indices = torch.topk(Y_Yt, k, dim=1)
        for i in range(Y_Yt.shape[0]):
            data_kernel[i, top_k_indices[i]] = 1
        return torch.maximum(data_kernel, data_kernel.T).numpy()
    elif dist == 'cosine' and knn_method == 'MKNN':
        Y_Yt = torch.from_numpy(Y @ Y.T)
        mask = torch.eye(Y_Yt.shape[0], dtype=bool)
        Y_Yt[mask] = -float('inf')
        data_kernel = torch.zeros_like(Y_Yt)
        _, top_k_indices = torch.topk(Y_Yt, k, dim=1)
        for i in range(Y_Yt.shape[0]):
            data_kernel[i, top_k_indices[i]] = 1
        return (data_kernel * data_kernel.T).numpy()


def main(embedding_path, distance, k, output_name, dimensions, knn_method):
    emb = np.genfromtxt(embedding_path, delimiter=',')[:, 2:]

    start_time = time.time()
    A = data_kernel(emb, k, distance, knn_method)
    middle_time = time.time()
    print("Data kernel running time (sec):", middle_time - start_time)

    if dimensions == 0:
        d = None
    else:
        d = dimensions

    ase = AdjacencySpectralEmbed(
        n_components=d,
        algorithm='truncated',
        check_lcc=False,
        diag_aug=False
    )
    Z = ase.fit_transform(A)
    end_time = time.time()
    print(f"ASE running time for d={d} (sec):", end_time - middle_time)
    np.savetxt(output_name, Z, delimiter=",")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='Create data kernel and latent position matrix from an embedding')
    parser.add_argument('embedding',
                            type=str,
                            help="The embedding")
    parser.add_argument('distance',
                            type=str,
                            help="The metric distance used to calculate the data kernel")    
    parser.add_argument('k',
                            type=int,
                            help="The number of neighbors for data kernel")
    parser.add_argument('output_name',
                            type=str,
                            help="The name of the output files")
    parser.add_argument('dimensions', 
                            type=int,
                            help="Desired dimensionality for the adjacency spectral embeddings")
    parser.add_argument('knn_method',
                            type=str,
                            choices=['KNN', 'MKNN'],
                            help="Wether to do KNN or mutual KNN for the graph construction")
    args = parser.parse_args()
    main(
        args.embedding,
        args.distance,
        args.k,
        args.output_name,
        args.dimensions,
        args.knn_method
    )