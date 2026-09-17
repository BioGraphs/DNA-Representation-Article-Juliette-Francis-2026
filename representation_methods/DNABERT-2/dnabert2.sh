#!/bin/bash

# Scripts directory
CURRENT_DIR=$PWD
DATA_DIR=${CURRENT_DIR}/Data
MODEL_DIR=${CURRENT_DIR}/representation_methods/DNABERT-2
SEQ_FILES=("bacteria_1")

for seq_file in "${SEQ_FILES[@]}"; do
	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Sequences file used: ${seq_file}_sequences.csv"
	python3 -W ignore $MODEL_DIR/dnabert2.py $DATA_DIR/Sequences/${seq_file}_sequences.csv $DATA_DIR/Embeddings/${seq_file}_dnabert2_embedding_bis.csv
	current_date_time=$(date)
	echo "Date and time at the end of the job: $current_date_time"
done
