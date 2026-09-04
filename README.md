# DNA Representation Article

Code to reproduce the results presented in "Graph-based comparison reveals distinct representation spaces across genomic foundation models":


---


## 1. Overview

The repository is organized in three sub-directory, `jaccard_distance`, `rdpg` and `plots`. The first two contain all the scripts to compare DNA representations with either the Jaccard distance metric, or the RDPG framework. DNA representation are available in the archive `Data.tar.gz` in the sub-directory `Embeddings`. The directory `plots` contains jupyter notebooks to generate the article figures. The numerotation of the corresponding figure is in the name of the notebook and detailed in the following table:

| Figure(s)      | Notebook                                                        | Description                                       |
|----------------|------------------------------------------------------------------|----------------------------------------------------|
| 1              | `taxonomic_tree_figure_1.ipynb`                                  | Taxonomic tree species of the DNA sequences                                     |
| 2              | `pca_projection_figure_2.ipynb`                                  | PCA projection of the representations                                     |
| 3, 5, S4       | `methods_distance_matrice_figure_3_and_5_and_S4.ipynb`           | Distance matrices for the representation methods                   |
| 4, S2          | `jaccard_heatmaps_figure_4_and_S2.ipynb`                         | Heatmaps showing Jaccard distance heatmaps                           |
| 6, S3          | `evidence_heatmaps_figure_6_and_S3.ipynb`                        | Heatmaps showing evidence of RDPG p-values                                  |
| S1             | `ani_figure_S1.ipynb`                                            | ANI depending on species representation distances                                          |
| S5             | `jaccard_and_rdpg_clusters_confusion_matrix_figure_S5.ipynb`     | Confusion matrix of Jaccard vs RDPG clusters         |
| S6             | todo     | todo         | Exploration of the results with various values of neighboors


Before running the notebooks, make sure you have run the comparison pipelines (Jaccard distance and RDPG framework) in their corresponding envirenments, as explained below or in the directories READMEs.

**Repository structure:**

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


## 2. Set up directories and envirenments 

### 2.1 Set up the working directory

The following command lines create a directory containing this Git repository, along with the data directory (uncompressed `Data.tar.gz`) and a results directory.
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

### 2.2 Set up RDPG framework envirenment
Please [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) if you do not have it already:
```
conda create --name rdpg python=3.12
conda activate rdpg
pip install graspologic==3.4.1
pip install future==1.0.0
pip install torch==2.6.0
pip install h5py==3.13.0
conda deactivate
```

### 2.3 Set up Jaccard distance metric envirenment
```
conda create --name embedding_comparator python=3.12
conda activate embedding_comparator
pip install -r ./dna_representation/jaccard_distance/embedding-comparator/requirements.txt
pip uninstall numpy
pip install numpy==2.0
pip install pandas
conda deactivate
```

## 4. Launch the comparison of the DNA representations with the RDPG framework

On a terminal, go into the `wd_dna_representation` directory and run the following command lines:
```bash
conda activate rdpg
./dna_representation_article/rdpg/compare_emb_with_rdpg.sh
```

## 5. Launch the comparison of the DNA representations with the Jaccard distance metric

On a terminal, go into the `wd_dna_representation` directory.

### 5.1 Prepare data and compute nearest neighbors
The DNA representations files (`.csv` in `./Data/Embeddings`) contain the DNA sequence, the species and the representation vectors, one sequence representation per line and columns are comma-separated.

The Jaccard distance metric uses [Embedding Comparator](https://github.com/mitvis/embedding-comparator), a visualisation tool, to compute nearest neighboors. To do so, representation files need to be in a specific format. The representation files should only contain the representations vectors, one representations per line and each dimension tab-separated (`.tsv`). A metadata file (`.tsv`) should contain the label of each representations (here it is *Seq-i-Spe-j*, i being the index of the sequence and j the index of the species), one per line, in the same order as the representation files. The script prepare_data.py do this step:
```bash
conda activate representations_comparator
python3 ./dna_representation_article/jaccard_distance/prepare_data.py ./dna_representation_article/jaccard_distance/embedding_paths.txt
```
`embedding_paths.txt` is a file containing path to the representations files (`.csv`) located in `./Data/Embeddings`.

Once data is in proper shape run `preprocess_data.sh`. The program preprocess_data.sh will execute `./dna_representation_article/jaccard_distance/embedding-comparator/preprocess_data.py` for every representation files, this script is from [Embedding Comparator](https://github.com/mitvis/embedding-comparator) tool.
The file preprocess_data.py computes the local neighborhoods of each sequence and dimensionality reduction with PCA, t-SNE, and UMAP, and write the output as JSON.

```bash
chmod +x ./dna_representation_article/jaccard_distance/preprocess_data.sh
./dna_representation_article/jaccard_distance/preprocess_data.sh
```

### 5.2 Run the comparision

Once nearest neighboors are identified, the Jaccard distance metric can be computed with the following command lines:
```bash
chmod +x ./dna_representation_article/jaccard_distance/jaccard_similarity.sh
./dna_representation_article/jaccard_distance/jaccard_similarity.sh
```