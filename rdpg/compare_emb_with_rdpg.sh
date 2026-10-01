#!/bin/bash

# RDPG hyperparameters
K=${1:-25}   # first positional argument; defaults to 25
N_BOOSTRAPS=999
D=0
DIST=euclidean
KNN_METHOD=KNN
HYPERPARAMETERS=${DIST}_${KNN_METHOD}_k-${K}_d-${D}

# Embeddings data sets and chosen embedding methods
EMBEDDING="bacteria_1"
MODELS=("hyenadna" "dnaberts" "tnf" "dnabert2" "dna2vec")

# Scripts directory
CURRENT_DIR=$PWD
RESULTS_DIR=${CURRENT_DIR}/Results/RDPG/
RDPG_DIR=${CURRENT_DIR}/rdpg/

# Embeddings directory
EMB_DIR=${CURRENT_DIR}/Data/Embeddings

# RDPG results directory
Z_DIR=${CURRENT_DIR}/Results/RDPG/latent_position_matrices
OMNIBUS_DIR=${CURRENT_DIR}/Results/RDPG/omnibus_latent_position_matrices
H0_DIR=${CURRENT_DIR}/Results/RDPG/h0_distributions
COMPARISON_DIR=${CURRENT_DIR}/Results/RDPG/embeddings_comparison_results


#________________________________________________________________________________________
echo "Step 1: Data Kernel and latent position matrix"
for model in "${MODELS[@]}"; do
	EMB=$EMB_DIR/${EMBEDDING}_${model}_embedding.csv
	OUTPUT_NAME=${Z_DIR}/${EMBEDDING}_${model}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_latent_position.csv
	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Embedding file used: ${EMBEDDING}_${model}_embedding.csv"
	python3 -W ignore $RDPG_DIR/data_kernel_latent_pos.py $EMB $DIST $K $OUTPUT_NAME $D $KNN_METHOD
	current_date_time=$(date)
	echo "Date and time at the end of the job: $current_date_time"
done


#________________________________________________________________________________________
echo "Step 2: Latent position matrix from omnibus matrix"
emb_list=()
for i in "${!MODELS[@]}"; do
    model="${MODELS[$i]}"
    emb_list+=("$EMB_DIR/${EMBEDDING}_${model}_embedding.csv")
done
emb_args=$(IFS=,; echo "${emb_list[*]}")

current_date_time=$(date)
echo "Date and time at the beginning of the job: $current_date_time"
python3 -W ignore $RDPG_DIR/omnibus_latent_pos.py $emb_args $K $OMNIBUS_DIR $DIST $D $KNN_METHOD #-m
current_date_time=$(date)
echo "Date and time at the end of the job: $current_date_time"


#________________________________________________________________________________________
echo "Step 3: Create H0 distributions"
for model in "${MODELS[@]}"; do

	EMB=$EMB_DIR/${EMBEDDING}_${model}_embedding.csv
	Z=${Z_DIR}/${EMBEDDING}_${model}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_latent_position.csv
	OUTPUT_PATH=${H0_DIR}/${EMBEDDING}_${model}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_h0_distributions.json
	OUTPUT_PATH_Z=${H0_DIR}/omnibus_latent_position_matrices/${EMBEDDING}_${model}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_h0_latent_positions

	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Embedding file used: ${EMBEDDING}_${model}_embedding.csv"
	python3 -W ignore $RDPG_DIR/create_h0_distributions.py $EMB $Z $K $N_BOOSTRAPS $OUTPUT_PATH $DIST $OUTPUT_PATH_Z $KNN_METHOD
	current_date_time=$(date)
	echo "Date and time at the end of the job: $current_date_time"
done


#________________________________________________________________________________________
echo "Step 4: Compare embeddings"
for model1 in "${MODELS[@]}"; do
    for model2 in "${MODELS[@]}"; do
        if [ "$model1" != "$model2" ]; then

        	Z1=${Z_DIR}/${EMBEDDING}_${model1}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_latent_position.csv
			OMNIBUS=${OMNIBUS_DIR}/${EMBEDDING}_${model1}_embedding_${EMBEDDING}_${model2}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_omnibus_latent_position.h5
			OUTPUT_FILE=${COMPARISON_DIR}/${EMBEDDING}_${model1}_vs_${model2}_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_embedding_comparison.json
			H0_DIST=${H0_DIR}/${EMBEDDING}_${model1}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_h0_distributions.json

			current_date_time=$(date)
			echo "Date and time at the begining of the job: $current_date_time"
			python3 -W ignore $RDPG_DIR/compare_emb_with_rdpg.py $Z1 $OMNIBUS $H0_DIST $OUTPUT_FILE
			current_date_time=$(date)
			echo "Date and time at the end of the job: $current_date_time"
        fi
    done
done


#________________________________________________________________________________________
echo "Step 5: Prepare results files for plots and analysis"
python3 -W ignore $RDPG_DIR/prepare_results_files_for_plots.py $COMPARISON_DIR $HYPERPARAMETERS $EMBEDDING ${RESULTS_DIR}
