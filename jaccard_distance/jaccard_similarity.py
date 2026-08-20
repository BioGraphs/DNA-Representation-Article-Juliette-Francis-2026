import numpy as np
import argparse
import pandas as pd
import json
from collections import defaultdict
import random
from pathlib import Path
import copy

def compute_iou_similarities(data1, data2, k, metric):
    """
    Compute the Intersection over Union (IoU) similarity between the k-nearest neighbors
    of two datasets (data1 and data2) using the specified distance metric.

    Args:
        data1 (list of dicts): A list where each element is a dictionary containing
                               the nearest neighbors (for each metric) for an embedding in data1.
        data2 (list of dicts): Same as data1, but for data2.
        k (int): The number of nearest neighbors to consider.
        metric (str): The metric (e.g., 'cosine', 'euclidean') to use for finding neighbors.

    Returns:
        list: A list of IoU similarity scores for each word/embedding pair between data1 and data2.
    """
    to_return = dict()

    for i in range(len(data1)):
        # Get the k-nearest neighbors for data1[i] and data2[i] based on the specified metric
        word1_neighbors = data1[i]['nearest_neighbors'][metric]['knn_ind'][:k]
        word1 = data1[i]['word']
        for j in range(len(data2)):
            if word1 == data2[j]['word']:
                word2_neighbors = data2[j]['nearest_neighbors'][metric]['knn_ind'][:k]
        # Compute the intersection and union of the neighbors
        intersection = set(word1_neighbors).intersection(set(word2_neighbors))
        union = set(word1_neighbors).union(set(word2_neighbors))

        # Compute the IoU (Intersection over Union)
        iou = len(intersection) / len(union) if len(union) > 0 else 0  # Avoid division by zero
        to_return[word1] = iou

    return to_return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                            prog='Jaccard similarity',
                            description=(""))
    parser.add_argument('model_1',
                            type=str,
                            help="The path to the model 1 file")
    parser.add_argument('model_2',
                            type=str,
                            help="The path to the model 2 file")
    parser.add_argument('k',
                            type=int,
                            help="The number of neighbors")
    parser.add_argument('distance',
                            type=str,
                            help="The metric distance used to calculate the nearest neighbors")    
    parser.add_argument('output_file',
                            type=str,
                            help="The path to the output file") 
    args = parser.parse_args()
    with open(args.model_1) as model_1, open(args.model_2) as model_2:
        model_1_results = json.load(model_1)
        model_2_results = json.load(model_2)
    similarity_scores = compute_iou_similarities(model_1_results, model_2_results, args.k, args.distance)
    pd.DataFrame([similarity_scores]).to_csv(args.output_file, sep="\t", index=False, header=True)
