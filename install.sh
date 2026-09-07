#!/bin/bash

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

conda create -n plots jupyterlab r-base -c conda-forge

conda create --name rdpg python=3.12
conda activate rdpg
pip install graspologic==3.4.1
pip install future==1.0.0
pip install torch==2.6.0
pip install h5py==3.13.0
conda deactivate

conda create --name embedding_comparator python=3.12
conda activate embedding_comparator
pip install -r ./dna_representation/jaccard_distance/embedding-comparator/requirements.txt
pip uninstall numpy
pip install numpy==2.0
pip install pandas
conda deactivate