# 1. Create a virtual environment

```bash
conda create --name embedding_comparator python=3.12
conda activate embedding_comparator
```

# 2. Set up environment

```bash
pip install -r jaccard_distance/embedding-comparator/requirements.txt
pip uninstall numpy
pip install numpy==2.0
pip install pandas
```

# 4. Prepare data and compute nearest neighbors
The embeddings file should contain the embedding vectors, one embedding per line and each dimension of embedding tab-separated.The metadata file should contain the label of each embedding, one per line, in the same order as embeddings_file. To do so, use the script prepare_data.py:
```bash
python3 ./dna_representation_article/jaccard_distance/prepare_data.py ./dna_representation_article/jaccard_distance/embedding_paths.txt
```
embedding_paths.txt is a file containing path to the embedding files created by embedding methods.

Once data is in proper shape run preprocess_data.sh. The program preprocess_data.sh will execute `./dna_representation_article/jaccard_distance/embedding-comparator/preprocess_data.py` for every embeddings, this script is from Embedding Comparator tool.
The file preprocess_data.py computes the local neighborhoods of each object in the embedding model and dimensionality reduction of all objects with PCA, t-SNE, and UMAP, and write the output as JSON.

```bash
chmod +x ./dna_representation_article/jaccard_distance/preprocess_data.sh
./dna_representation_article/jaccard_distance/preprocess_data.sh
```

# 5. Compute Jaccard distance

```bash
chmod +x ./dna_representation_article/jaccard_distance/jaccard_similarity.sh
./dna_representation_article/jaccard_distance/jaccard_similarity.sh
```
