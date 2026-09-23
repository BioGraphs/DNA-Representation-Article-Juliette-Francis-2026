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
# The `plots` env holds everything needed to run the notebooks: JupyterLab (pip)
# and a pinned R 4.4.3 with its IRkernel plus the R packages used by the figures,
# all installed from conda-forge binary packages (fast, no source compilation).
#
# NOTE: ggtree and ggtreeExtra (used by the taxonomic tree, figure 1) are NOT
# installed here: they are not available on conda-forge and compiling them in a
# conda R env is fragile. They must be installed separately if figure 1 is needed.
R_PACKAGES=(
  r-ggplot2=4.0.3
  r-dplyr=1.2.1
  r-glue=1.8.1
  r-rcolorbrewer=1.1_3
  r-dendextend=1.19.1
  r-patchwork=1.3.2
  r-circlize=0.4.18
  r-rstatix=1.1.0
  r-reshape2=1.4.5
  r-ggbreak=0.1.7
  r-stringr=1.6.0
  r-tidyr=1.3.2
  r-plotly=4.12.1
  r-ggforce=0.5.0
  r-purrr=1.2.2
  r-gplots=3.3.0
  r-jsonlite=2.0.0
  r-aricode=1.1.0
  r-readr=2.2.0
  r-ade4=1.7_24
  r-gridextra=2.3.1
  r-cluster=2.1.8.3
)
ensure_env plots jupyterlab r-base=4.4.3 r-irkernel r-remotes r-biocmanager "${R_PACKAGES[@]}" -c conda-forge
conda run --no-capture-output -n plots pip install -r ${CURRENT_DIR}/requirements_plots.txt
# Register the R kernel of the `plots` env (points at envs/plots/bin/R)
conda run --no-capture-output -n plots Rscript -e 'IRkernel::installspec()'

ensure_env rdpg python=3.12
conda run --no-capture-output -n rdpg pip install -r ${CURRENT_DIR}/requirements_rdpg.txt

ensure_env embedding_comparator python=3.12
conda run --no-capture-output -n embedding_comparator pip install -r ${CURRENT_DIR}/requirements_embedding_comparator.txt
# Force numpy to the version required by the embedding-comparator tool
conda run --no-capture-output -n embedding_comparator pip install "numpy==2.0.0"

echo "=== Installation complete ==="
