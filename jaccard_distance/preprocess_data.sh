#!/bin/bash

DATA=bacteria_1

mkdir ./dna_representation_article/jaccard_distance/embedding-comparator/data/${DATA}

WORKING_DIR=./dna_representation_article/jaccard_distance
DATA_DIR=./Results/Jaccard_distance/${DATA}
OUTPUT_DIR=./dna_representation_article/jaccard_distance/embedding-comparator/data/${DATA}

mkdir $DATA_DIR/embedding_comparator_results

MODELS=("hyenadna" "dnaberts" "tnf" "dnabert2" "dna2vec")

for MODEL in "${MODELS[@]}"; do
          
          python3 $WORKING_DIR/embedding-comparator/preprocess_data.py \
            --embeddings_file=$DATA_DIR/embeddings_in_tsv_format/${DATA}_${MODEL}_embedding.tsv \
            --metadata_file=$DATA_DIR/embeddings_in_tsv_format/sequence_id.tsv \
            --outfile=$OUTPUT_DIR/${DATA}_${MODEL}_embedding.json \
            --max_k=70

done

mv $OUTPUT_DIR/* $DATA_DIR/embedding_comparator_results
rmdir $OUTPUT_DIR