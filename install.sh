#!/bin/bash

init() {
    set -e
    CURRENT_DIR=$PWD
    RESULTS_DIR=${CURRENT_DIR}/Results/

    # Setup results directory
    tar -xvzf ${CURRENT_DIR}/Data.tar.gz -C ${CURRENT_DIR}
    mkdir ${RESULTS_DIR}
    mkdir ${RESULTS_DIR}/RDPG
    mkdir ${RESULTS_DIR}/RDPG/latent_position_matrices
    mkdir ${RESULTS_DIR}/RDPG/omnibus_latent_position_matrices
    mkdir ${RESULTS_DIR}/RDPG/h0_distributions
    mkdir ${RESULTS_DIR}/RDPG/embeddings_comparison_results
    mkdir ${RESULTS_DIR}/Plots
    mkdir ${RESULTS_DIR}/Jaccard_distance
}

cleanup() {
    rm -rf ${RESULTS_DIR}
}


create_environments() {
    # Check that conda is available
    if ! command -v conda &> /dev/null; then
        echo "Error: conda is not installed or not in the PATH."
        exit 1
    fi

    echo "=== Creating environment 'plots' ==="
    conda create -y -n plots jupyterlab r-base -c conda-forge

    echo "=== Creating environment 'rdpg' ==="
    conda create -y -n rdpg python=3.12
    conda run --no-capture-output -n rdpg pip install graspologic==3.4.1
    conda run --no-capture-output -n rdpg pip install future==1.0.0
    conda run --no-capture-output -n rdpg pip install torch==2.6.0
    conda run --no-capture-output -n rdpg pip install h5py==3.13.0

    echo "=== Creating environment 'embedding_comparator' ==="
    conda create -y -n embedding_comparator python=3.12
    conda run --no-capture-output -n embedding_comparator pip install -r ${CURRENT_DIR}/jaccard_distance/embedding-comparator/requirements.txt
    conda run --no-capture-output -n embedding_comparator pip uninstall -y numpy
    conda run --no-capture-output -n embedding_comparator pip install numpy==2.0
    conda run --no-capture-output -n embedding_comparator pip install pandas
}


main() {
    init

    # Set a trap to call cleanup on error
    trap cleanup ERR

    create_environments
    echo "=== Installation complete ==="

}

main && exit 0
