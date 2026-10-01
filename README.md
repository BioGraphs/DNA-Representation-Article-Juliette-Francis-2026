# DNA Representation Article

**TL;DR** — Reproducible code for "Graph-based comparison reveals distinct
representation spaces across genomic foundation models". Two pipelines compare
DNA representations (Jaccard, RDPG); three conda envs. Quick start: Docker
(`docker build` + `docker run`) → run the Jaccard and RDPG comparisons →
then `plots/` notebooks.


---


## 1. Overview

The repository is organized in five sub-directories, `jaccard_distance`, `rdpg`, `plots`, `representation_methods`, and `docker`. The first two contain all the scripts needed to compare DNA representations with either the Jaccard distance metric, or the RDPG framework. DNA representation made with TNF (Tetra-Nucleotide Frequency), [dna2vec](https://github.com/pnpnpn/dna2vec), [HyenaDNA](https://github.com/HazyResearch/hyena-dna), [DNABERT-2](https://github.com/MAGICS-LAB/DNABERT_2) and [DNABERT-S](https://github.com/MAGICS-LAB/DNABERT_S) are available in the archive `Data.tar.gz` in the sub-directory `Embeddings`. The directory `plots` contains jupyter notebooks to generate the article figures. The numerotation of the corresponding figure is in the name of the notebook and detailed in the following table:

<details>
<summary>Click to expand</summary>

| Figure(s)      | Notebook                                                        | Description                                       |
|----------------|------------------------------------------------------------------|----------------------------------------------------|
| 1              | `taxonomic_tree_figure_1.ipynb`                                  | Taxonomic tree of DNA sequences species                                      |
| 2              | `pca_projection_figure_2.ipynb`                                  | PCA projection of the representations                                     |
| 3, 5, S4       | `methods_distance_matrice_figures_3_and_5_and_S4.ipynb`           | Distance matrices for the representation methods                   |
| 4, S2          | `jaccard_heatmaps_figures_4_and_S2.ipynb`                         | Heatmaps showing Jaccard distance heatmaps                           |
| 6, S3          | `evidence_heatmaps_figures_6_and_S3.ipynb`                        | Heatmaps showing evidence of RDPG p-values                                  |
| S1             | `ani_figure_S1.ipynb`                                            | ANI depending on species representation distances                                          |
| S5             | `jaccard_and_rdpg_clusters_confusion_matrix_figure_S5.ipynb`     | Confusion matrix of Jaccard vs RDPG clusters         |
| S6             | `k_value_exploration_figure_S6.ipynb`                            | Exploration of the results with various values of neighboors |

</details>

**Before running the notebooks, make sure you have run the comparison pipelines** (Jaccard distance and RDPG framework) in their corresponding environments, as explained below.


**Re-compute DNA sequence representations (not mandatory to reproduce the article results):** To simplify analysis, and since regenerating them would not add anything new on our part, the DNA sequence representations for our dataset are provided directly in the `Data.tar.gz` archive. However, if you wish to generate them yourself, the code we used is available in the `representation_methods` directory. Each sub-directory corresponds to one method, and the scripts were written following the documentation found on that method's GitHub page. Instructions for setting up the environment for each method can be found in the corresponding sub-directory's README. To avoid overwriting the existing representation files, any representation you generate will have the same filename with the suffix `_bis` appended. Note that [DNABERT-S](https://github.com/MAGICS-LAB/DNABERT_S) inference can be time-consuming if you don't have a GPU.


**Repository structure:**
<details>
<summary>Click to expand</summary>

```bash
.
├── Data.tar.gz # Data archive
├── install.sh # Set up packages and directories
├── requirements_rdpg.txt # Conda deps for the `rdpg` env
├── requirements_embedding_comparator.txt # Conda deps for the `embedding_comparator` env
├── README.md
├── docker # Reproducible environments-only Docker image (repo is bind-mounted)
│   ├── Dockerfile
│   ├── README.md
│   └── scripts
│       └── docker-entrypoint.sh
├── jaccard_distance # Scripts to compare DNA representations with the Jaccard distance
│   ├── embedding-comparator # Submodule
│   ├── embedding_paths.txt
│   ├── jaccard_similarity.py
│   ├── jaccard_similarity.sh
│   ├── prepare_data.py
│   └── preprocess_data.sh
├── plots # Notebooks to reproduce figures
│   ├── ani_figure_S1.ipynb
│   ├── evidence_heatmaps_figures_6_and_S3.ipynb
│   ├── jaccard_and_rdpg_clusters_confusion_matrix_figure_S5.ipynb
│   ├── jaccard_heatmaps_figures_4_and_S2.ipynb
│   ├── k_value_exploration_figure_S6.ipynb
│   ├── methods_distance_matrice_figures_3_and_5_and_S4.ipynb
│   ├── pca_projection_figure_2.ipynb
│   └── taxonomic_tree_figure_1.ipynb
├── rdpg # Scripts to compare DNA representations with the RDPG framework
│   ├── compare_emb_with_rdpg.py
│   ├── compare_emb_with_rdpg.sh
│   ├── create_h0_distributions.py
│   ├── data_kernel_latent_pos.py
│   ├── omnibus_latent_pos.py
│   └── prepare_results_files_for_plots.py
└── representation_methods # Scripts to create DNA representations
    ├── DNABERT-2
    │   ├── dnabert2.py
    │   ├── dnabert2.sh
    │   ├── requirements.txt
    │   └── README.md
    ├── DNABERT-S
    │   ├── dnaberts.py
    │   ├── dnaberts.sh
    │   ├── requirements.txt
    │   └── README.md
    ├── TNF
    │   ├── TNF.py
    │   ├── TNF.sh
    │   └── README.md
    ├── dna2vec
    │   ├── DNA2VEC.py
    │   ├── DNA2VEC.sh
    │   ├── README.md
    │   └── dna2vec # Submodule
    └── hyenadna
        ├── hyenadna.py
        ├── hyenadna.sh
        ├── README.md
        ├── hyena-dna # Submodule
        └── hyenadna-small-32k-seqlen # Submodule
```

</details>

## 2. Set up directories and environments for the comparison of representations

First, clone the repository and initialise its submodules.
```bash
git clone https://forge.inrae.fr/holobionts_pepr/workpackage_1/dna_representation_article.git
cd dna_representation_article
git submodule update --init --recursive
```

Then you can manage dependancies with either the docker setup (section 2.1) or the manual installation (section 2.2).

### 2.1 Docker (recommended)

Please [install Docker](https://docs.docker.com/engine/install/) if you do not have it already.

This is the easiest way to get started: the image provides the three conda environments (`rdpg`, `embedding_comparator`, `plots`) without installing conda/R on your machine and having to manage conflicts. Full details are in [`docker/README.md`](docker/README.md).

From the repository root:
```bash
docker build -t dna-article:ubuntu26.04 -f docker/Dockerfile .
```

Run interactively, mounting the current repo:
```bash
docker run --rm -it \
  -p 8888:8888 \
  -v "$PWD:/workspace" \
  dna-article:ubuntu26.04 bash
```
The `-p 8888:8888` forwards the container's port 8888 to your host; it is useful later for the JupyterLab notebook server (section 5).

You land in `/workspace` with the three environments ready. The environment activation commands described in sections 3, 4 and 5 apply inside the container, you can direclty go to section 3.

### 2.2 Manual installation

Please [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) if you do not have it already.

From the repository root:
```bash
chmod +x install.sh
./install.sh # creates the data directory (uncompressed `Data.tar.gz`), a results directory, and three conda environments (`rdpg`, `embedding_comparator`, `plots`).
```

## 3. Launch the comparison of the DNA representations with the RDPG framework

From the repository root (in the container or not):
```bash
conda activate rdpg
./rdpg/compare_emb_with_rdpg.sh
```

Be aware that `compare_emb_with_rdpg.sh` runs the RDPG framework for only one value of k (25 by default), but the results needed for the Figure S6 involve running the script with other values (5, 10, 40, 55, 70). The script takes the value of `K` as its first positional argument (defaults to 25), so to be able to run the `k_value_exploration_figure_S6.ipynb` notebook you need to run it once per k value (5, 10, 40, 55, 70). For the standard comparison, just run it with the default:

```bash
./rdpg/compare_emb_with_rdpg.sh        # k=25 (default)
```

For figure S6, run one k value at a time, for example:

```bash
./rdpg/compare_emb_with_rdpg.sh 5      # k=5
```

and repeat for the other values (10, 40, 55, 70).


## 4. Launch the comparison of the DNA representations with the Jaccard distance metric

### 4.1 Prepare data and compute nearest neighbors
The DNA representations files (`.csv` in `./Data/Embeddings`) contain the DNA sequences, the species and the representation vectors, one sequence representation per line and columns are comma-separated.

The Jaccard distance metric uses [Embedding Comparator](https://github.com/mitvis/embedding-comparator), a visualisation tool, to compute nearest neighboors. To do so, representation files need to be in a specific format. The representation files should only contain the representations vectors, one representations per line and each dimension tab-separated (`.tsv`). A metadata file (`.tsv`) should contain the label of each representations (here it is *Seq-i-Spe-j*, i being the index of the sequence and j the index of the species), one per line, in the same order as the representation files. The script prepare_data.py do this step.

From the repository root (in the container or not):
```bash
conda activate embedding_comparator
python3 ./jaccard_distance/prepare_data.py ./jaccard_distance/embedding_paths.txt
```
`embedding_paths.txt` is a file containing path to the representations files (`.csv`) located in `./Data/Embeddings`.

Once data is in proper shape runs `preprocess_data.sh`. The program preprocess_data.sh will execute `./dna_representation_article/jaccard_distance/embedding-comparator/preprocess_data.py` for every representation files, this script is from [Embedding Comparator](https://github.com/mitvis/embedding-comparator) tool.
The file preprocess_data.py computes the local neighborhoods of each sequence and dimensionality reduction with PCA, t-SNE, and UMAP, and write the output as JSON.

```bash
./jaccard_distance/preprocess_data.sh
```

### 4.2 Run the comparision

Once nearest neighboors are identified, the Jaccard distance metric can be computed with the following command lines:
```bash
./jaccard_distance/jaccard_similarity.sh
```


## 5. Analyze results with the notebooks

From the repository root:
```bash
conda activate plots
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root # if you are using Docker. Otherwise, write only "jupyter lab".
```
Then open `http://localhost:8888` (the token is shown in the terminal).

> **Tip:** check the requierements column in the notebook table before executing any notebook.
