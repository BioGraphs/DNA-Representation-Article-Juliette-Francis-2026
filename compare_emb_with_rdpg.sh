#!/bin/bash

#SBATCH --job-name=compare_embeddings_with_rdpg
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --output=compare_embeddings_with_rdpg.log
#SBATCH --error=compare_embeddings_with_rdpg.err

source /local/env/envconda.sh
conda activate metric_rdpg


K=25
N_BOOSTRAPS=999
D=0
DIST=euclidean
KNN_METHOD=KNN
RESULTS_SUB_DIR="article_results/"
EMBEDDING="bacteria_4"
MODELS=("hyenadna" "dnaberts" "bag4mers" "dnabert2" "dna2vec")


WORKING_DIR=/home/genouest/cnrs_umr6074/jfrancis/phd_juliette_francis/dna_embedding/metric_rdpg
EMB_DIR=/home/genouest/cnrs_umr6074/jfrancis/Results/dnaberts_synthetic_data_embeddings/reference/article_embeddings
Z_DIR=/home/genouest/cnrs_umr6074/jfrancis/Results/dnaberts_synthetic_data_results_rdpg_metric/${RESULTS_SUB_DIR}${EMBEDDING}/latent_position_matrices
OMNIBUS_DIR=/home/genouest/cnrs_umr6074/jfrancis/Results/dnaberts_synthetic_data_results_rdpg_metric/${RESULTS_SUB_DIR}${EMBEDDING}/omnibus_latent_position_matrices
H0_DIR=/home/genouest/cnrs_umr6074/jfrancis/Results/dnaberts_synthetic_data_results_rdpg_metric/${RESULTS_SUB_DIR}${EMBEDDING}/h0_distributions
COMPARISON_DIR=/home/genouest/cnrs_umr6074/jfrancis/Results/dnaberts_synthetic_data_results_rdpg_metric/${RESULTS_SUB_DIR}${EMBEDDING}/embeddings_comparison_results


#________________________________________________________________________________________
echo "Step 1: Data Kernel and latent position matrix"
for model in "${MODELS[@]}"; do
	EMB=$EMB_DIR/${EMBEDDING}_${model}_embedding.csv
	OUTPUT_NAME=${Z_DIR}/${EMBEDDING}_${model}_embedding_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_latent_position.csv
	current_date_time=$(date)
	echo "Date and time at the begining of the job: $current_date_time"
	echo "Embedding file used: ${EMBEDDING}_${model}_embedding.csv"
	/usr/bin/time -v python3 -W ignore $WORKING_DIR/data_kernel_latent_pos.py $EMB $DIST $K $OUTPUT_NAME $D $KNN_METHOD
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
/usr/bin/time -v python3 -W ignore $WORKING_DIR/omnibus_latent_pos.py $emb_args $K $OMNIBUS_DIR $DIST $D $KNN_METHOD #-m
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
	/usr/bin/time -v python3 -W ignore $WORKING_DIR/create_h0_distributions.py $EMB $Z $K $N_BOOSTRAPS $OUTPUT_PATH $DIST $OUTPUT_PATH_Z $KNN_METHOD #-m
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
			/usr/bin/time -v python3 -W ignore $WORKING_DIR/compare_emb_with_rdpg.py $Z1 $OMNIBUS $H0_DIST $OUTPUT_FILE
			current_date_time=$(date)
			echo "Date and time at the end of the job: $current_date_time"
        fi
    done
done


mv compare_embeddings_with_rdpg.log ./output_error/${EMBEDDING}_embeddings_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_comparison.log
mv compare_embeddings_with_rdpg.err ./output_error/${EMBEDDING}_embeddings_${DIST}_${KNN_METHOD}_k-${K}_d-${D}_comparison.err

