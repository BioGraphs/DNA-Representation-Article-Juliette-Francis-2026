#!/bin/bash

SEQ_FILES=("bacteria_1")

for seq_file in "${SEQ_FILES[@]}"; do
  current_date_time=$(date)
  current_date=$(date +"%Y-%m-%d_%H-%M-%S")
  echo "Date and time at the beginning of the job: $current_date_time"

  apptainer exec \
    --bind ../../Data:/Data \
    --bind "$(pwd)":/hyenadna \
    hyena-dna_latest.sif \
    python3 /hyenadna/hyenadna.py /Data/Sequences/${seq_file}_sequences.csv /Data/Embeddings/${seq_file}_hyenadna_embedding_bis.csv

  current_date_time=$(date)
  echo "Date and time at the end of the job: $current_date_time"
done
