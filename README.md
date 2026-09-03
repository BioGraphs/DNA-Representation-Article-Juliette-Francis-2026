# DNA Representation Article

Code to reproduce the results presented in "Graph-based comparison of genomic foundation models]{Graph-based comparison reveals distinct representation spaces across genomic foundation models":


---

## Overview


## Repository structure

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
