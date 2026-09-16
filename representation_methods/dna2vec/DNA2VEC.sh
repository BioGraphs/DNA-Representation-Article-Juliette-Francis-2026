#!/bin/bash

# Scripts directory
CURRENT_DIR=$PWD
DATA_DIR=${CURRENT_DIR}/Data
MODEL_DIR=${CURRENT_DIR}/representation_methods/dna2vec
WEIGHTS=${CURRENT_DIR}/representation_methods/dna2vec/dna2vec/pretrained/dna2vec-20161219-0153-k3to8-100d-10c-29320Mbp-sliding-Xat.w2v
k=4
SEQ_FILES=("bacteria_1")

for seq_file in "${SEQ_FILES[@]}"; do
	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Sequences file used: ${seq_file}_sequences.csv"
	python3 -W ignore $MODEL_DIR/DNA2VEC.py $DATA_DIR/Sequences/${seq_file}_sequences.csv $DATA_DIR/Embeddings/${seq_file}_dna2vec_embedding_bis.csv $k $WEIGHTS
	current_date_time=$(date)
	echo "Date and time at the end of the job: $current_date_time"
done
