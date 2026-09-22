#!/bin/bash
set -e

CURRENT_DIR=$PWD
RESULTS_DIR=${CURRENT_DIR}/Results/

# ____ Helper: create a conda env if it does not already exist
conda_env_exists() {
    conda env list | awk '{print $1}' | grep -qx "$1"
}

ensure_env() {
    local name=$1
    shift
    if conda_env_exists "$name"; then
        echo "=== Environment '$name' already exists, skipping creation ==="
    else
        echo "=== Creating environment '$name' ==="
        conda create -y -n "$name" "$@"
    fi
}

# ____ 1. Unpack data (idempotent: skip if already unpacked)
if [ -d "${CURRENT_DIR}/Data/Embeddings" ]; then
    echo "=== Data/Embeddings already present, skipping extraction ==="
else
    echo "=== Extracting Data.tar.gz ==="
    tar -xvzf ${CURRENT_DIR}/Data.tar.gz -C ${CURRENT_DIR}
fi

# ____ 2. Create results directory tree (mkdir -p makes this idempotent)
echo "=== Creating Results directory tree ==="
mkdir -p ${RESULTS_DIR}/RDPG/latent_position_matrices
mkdir -p ${RESULTS_DIR}/RDPG/omnibus_latent_position_matrices
mkdir -p ${RESULTS_DIR}/RDPG/h0_distributions
mkdir -p ${RESULTS_DIR}/RDPG/embeddings_comparison_results
mkdir -p ${RESULTS_DIR}/Plots
mkdir -p ${RESULTS_DIR}/Jaccard_distance

# ____ 3. Create conda environments (idempotent)
ensure_env plots jupyterlab r-base -c conda-forge
conda run --no-capture-output -n plots pip install -r ${CURRENT_DIR}/requirements_plots.txt

ensure_env rdpg python=3.12
conda run --no-capture-output -n rdpg pip install -r ${CURRENT_DIR}/requirements_rdpg.txt

ensure_env embedding_comparator python=3.12
conda run --no-capture-output -n embedding_comparator pip install -r ${CURRENT_DIR}/requirements_embedding_comparator.txt
# Force numpy to the version required by the embedding-comparator tool
conda run --no-capture-output -n embedding_comparator pip install "numpy==2.0.0"

echo "=== Installation complete ==="
