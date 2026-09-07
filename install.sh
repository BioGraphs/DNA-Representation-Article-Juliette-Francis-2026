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
