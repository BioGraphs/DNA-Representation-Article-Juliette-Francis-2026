# DNA Representation Article

Code to reproduce the results presented in "Graph-based comparison of genomic foundation models]{Graph-based comparison reveals distinct representation spaces across genomic foundation models":


---

## 1. Set up directories and envirenments 

### 1.1 Set up the working directory
```
mkdir wd_dna_representation
cd wd_dna_representation
mkdir Results
git clone https://forge.inrae.fr/holobionts_pepr/workpackage_1/dna_representation_article.git
tar -xvzf ./dna_representation_article/Data.tar.gz -C ./
cd dna_representation_article
git submodule update --init --recursive
cd ../
mkdir ./Results/RDPG
mkdir ./Results/RDPG/latent_position_matrices
mkdir ./Results/RDPG/omnibus_latent_position_matrices
mkdir ./Results/RDPG/h0_distributions
mkdir ./Results/RDPG/embeddings_comparison_results
mkdir ./Results/Plots
mkdir ./Results/Jaccard_distance
```

### 1.2 Set up RDPG framework envirenment
```
conda create --name rdpg python=3.12
conda activate rdpg
pip install graspologic==3.4.1
pip install future==1.0.0
pip install torch==2.6.0
pip install h5py==3.13.0
conda deactivate
```

### 1.3 Set up Jaccard distance metric envirenment
```
conda create --name embedding_comparator python=3.12
conda activate embedding_comparator
pip install -r ./dna_representation/jaccard_distance/embedding-comparator/requirements.txt
pip uninstall numpy
pip install numpy==2.0
pip install pandas
conda deactivate
```

## 2. Overview


## 3. Repository structure

```
.
├── Data.tar.gz               # Data archive
├── README.md
├── jaccard_distance               # Scripts to compare DNA representations with the Jaccard distance
│   ├── README.md
│   ├── embedding-comparator
│   ├── embedding_paths.txt
│   ├── jaccard_similarity.py
│   ├── jaccard_similarity.sh
│   ├── prepare_data.py
│   └── preprocess_data.sh
├── plots               # Notebooks to reproduce figures
│   ├── ani_figure_S1.ipynb
│   ├── evidence_heatmaps_figure_6_and_S3.ipynb
│   ├── jaccard_and_rdpg_clusters_confusion_matrix_figure_S5.ipynb
│   ├── jaccard_heatmaps_figure_4_and_S2.ipynb
│   ├── methods_distance_matrice_figure_3_and_5_and_S4.ipynb
│   ├── pca_projection_figure_2.ipynb
│   └── taxonomic_tree_figure_1.ipynb
├── rdpg               # Scripts to compare DNA representations with the RDPG framework
│   ├── README.md
│   ├── compare_emb_with_rdpg.py
│   ├── compare_emb_with_rdpg.sh
│   ├── create_h0_distributions.py
│   ├── data_kernel_latent_pos.py
│   ├── omnibus_latent_pos.py
│   └── prepare_results_files_for_plots.py
```

## 4. Launch the comparison of the DNA representations with the RDPG framework

On a terminal, go into the `wd_dna_representation` directory an run the following command lines:
```bash
conda activate rdpg
./dna_representation_article/rdpg/compare_emb_with_rdpg.sh
```

## 5. Launch the comparison of the DNA representations with the Jaccard distance metric

On a terminal, go into the `wd_dna_representation` directory.

### 5.1 Prepare data and compute nearest neighbors
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

### 5.2 Run the comparision

```bash
chmod +x ./dna_representation_article/jaccard_distance/jaccard_similarity.sh
./dna_representation_article/jaccard_distance/jaccard_similarity.sh
```