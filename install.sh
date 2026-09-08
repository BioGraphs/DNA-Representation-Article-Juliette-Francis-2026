#!/bin/bash
set -e

cd ../
mkdir wd_dna_representation
mv ./dna_representation_article ./wd_dna_representation/dna_representation_article
cd wd_dna_representation
tar -xvzf ./dna_representation_article/Data.tar.gz -C ./
mkdir Results
mkdir ./Results/RDPG
mkdir ./Results/RDPG/latent_position_matrices
mkdir ./Results/RDPG/omnibus_latent_position_matrices
mkdir ./Results/RDPG/h0_distributions
mkdir ./Results/RDPG/embeddings_comparison_results
mkdir ./Results/Plots
mkdir ./Results/Jaccard_distance


# Check that conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in the PATH."
    exit 1
fi

echo "=== Creating environment 'plots' ==="
conda create -y -n plots jupyterlab r-base -c conda-forge

echo "=== Creating environment 'rdpg' ==="
conda create -y --name rdpg python=3.12
conda run --no-capture-output -n rdpg pip install graspologic==3.4.1
conda run --no-capture-output -n rdpg pip install future==1.0.0
conda run --no-capture-output -n rdpg pip install torch==2.6.0
conda run --no-capture-output -n rdpg pip install h5py==3.13.0

echo "=== Creating environment 'embedding_comparator' ==="
conda create -y --name embedding_comparator python=3.12
conda run --no-capture-output -n embedding_comparator pip install -r ./dna_representation_article/jaccard_distance/embedding-comparator/requirements.txt
conda run --no-capture-output -n embedding_comparator pip uninstall -y numpy
conda run --no-capture-output -n embedding_comparator pip install numpy==2.0
conda run --no-capture-output -n embedding_comparator pip install pandas

echo "=== Installation complete ==="