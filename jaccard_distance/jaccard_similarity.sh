#!/bin/bash

DATA=bacteria_1
WORKING_DIR=./dna_representation_article/jaccard_distance
DATA_DIR=./Results/Jaccard_distance/${DATA}/embedding_comparator_results
OUTPUT_DIR=./Results/Jaccard_distance/${DATA}/jaccard_results

mkdir ${OUTPUT_DIR}

K_VALUES=(5 10 25 40 55 70)
DISTANCE=euclidean
MODELS=("hyenadna" "dnaberts" "tnf" "dnabert2" "dna2vec")

for k in "${K_VALUES[@]}"; do
    for ((i = 0; i < ${#MODELS[@]}; i++)); do
        for ((j = i + 1; j < ${#MODELS[@]}; j++)); do
            MODEL1=${MODELS[i]}
            MODEL2=${MODELS[j]}
            INPUT_FILE1=${DATA_DIR}/${DATA}_${MODEL1}_embedding.json
            INPUT_FILE2=${DATA_DIR}/${DATA}_${MODEL2}_embedding.json
            OUTPUT_FILE=${OUTPUT_DIR}/${DATA}_${MODEL1}_${MODEL2}_jaccard_similarity_k-${k}.csv
            current_date_time=$(date)
            echo "Date and time at the beginning of the job: $current_date_time"
            python3 $WORKING_DIR/jaccard_similarity.py \
                $INPUT_FILE1 \
                $INPUT_FILE2 \
                $k \
                $DISTANCE \
                $OUTPUT_FILE
            current_date_time=$(date)
            echo "Date and time at the end of the job: $current_date_time"
        done
    done
done
