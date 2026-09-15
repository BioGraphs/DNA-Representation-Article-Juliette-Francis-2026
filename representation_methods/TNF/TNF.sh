#!/bin/bash

# Scripts directory
CURRENT_DIR=$PWD
DATA_DIR=${CURRENT_DIR}/Data
MODEL_DIR=${CURRENT_DIR}/representation_methods/TNF

k=4
SEQ_FILES=("bacteria_1")

for seq_file in "${SEQ_FILES[@]}"; do
	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Sequences file used: ${seq_file}.tsv"
	python3 -W ignore $MODEL_DIR/TNF.py $DATA_DIR/Sequences/${seq_file}_sequences.csv $DATA_DIR/Embeddings/${seq_file}_tnf_embedding_bis.csv $k
	current_date_time=$(date)
	echo "Date and time at the end of the job: $current_date_time"
done
