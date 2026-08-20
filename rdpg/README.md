# 1. Create a virtual environment

```bash
conda create --name rdpg python=3.12
conda activate rdpg
```

# 2. Set up environment

```bash
pip install graspologic==3.4.1
pip install future==1.0.0
pip install torch==2.6.0
pip install h5py==3.13.0
```

# 3. Launch the comparison of the DNA representations

Go into the directory that contains the dna_representation_article repository and the Results directory. Do these following commands:
```bash
mkdir ./Results/RDPG
mkdir ./Results/RDPG/latent_position_matrices
mkdir ./Results/RDPG/omnibus_latent_position_matrices
mkdir ./Results/RDPG/h0_distributions
mkdir ./Results/RDPG/embeddings_comparison_results
```

```bash
conda activate rdpg
./dna_representation_article/rdpg/compare_emb_with_rdpg.sh
```