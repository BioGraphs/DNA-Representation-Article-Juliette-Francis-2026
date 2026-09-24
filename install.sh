#!/bin/bash
set -e

# Usage:
#   ./install.sh                 # full install: data + results tree + conda envs (default)
#   ./install.sh --envs-only     # only create the conda environments (skip data/results)
#   ./install.sh --data-only     # only unpack Data.tar.gz + create the Results/ tree
#
# Used by the Docker build to install only the envs into the image (the repo and
# data are bind-mounted at runtime) and by the container entrypoint to set up
# the host Data/ and Results/ automatically.

FULL=0
ENVS_ONLY=0
DATA_ONLY=0
case "$1" in
    --envs-only) ENVS_ONLY=1 ;;
    --data-only) DATA_ONLY=1 ;;
    ""|--full)   FULL=1 ;;
    *)
        echo "Usage: $0 [--envs-only|--data-only|--full]" >&2
        exit 1
        ;;
esac

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

# ____ 1+2. Unpack data + create results tree (skipped with --envs-only)
if [ "${ENVS_ONLY}" = "1" ]; then
    echo "=== Skipping data unpack and Results tree (envs-only) ==="
else
    # Unpack data (idempotent: skip if already unpacked)
    if [ -d "${CURRENT_DIR}/Data/Embeddings" ]; then
        echo "=== Data/Embeddings already present, skipping extraction ==="
    else
        echo "=== Extracting Data.tar.gz ==="
        tar -xvzf ${CURRENT_DIR}/Data.tar.gz -C ${CURRENT_DIR}
    fi

    # Create results directory tree (mkdir -p makes this idempotent)
    echo "=== Creating Results directory tree ==="
    mkdir -p ${RESULTS_DIR}/RDPG/latent_position_matrices
    mkdir -p ${RESULTS_DIR}/RDPG/omnibus_latent_position_matrices
    mkdir -p ${RESULTS_DIR}/RDPG/h0_distributions
    mkdir -p ${RESULTS_DIR}/RDPG/embeddings_comparison_results
    mkdir -p ${RESULTS_DIR}/Plots
    mkdir -p ${RESULTS_DIR}/Jaccard_distance
fi

# ____ 3. Create conda environments (idempotent; skipped with --data-only)
if [ "${DATA_ONLY}" = "1" ]; then
    echo "=== Skipping conda environment creation (data-only) ==="
else
# The `plots` env holds everything needed to run the notebooks: JupyterLab
# and a pinned R 4.5.3 with its IRkernel plus the R packages used by the figures,
# all installed as precompiled conda binaries (fast, no source compilation).
# The tidyverse is installed as the single r-tidyverse meta-package (rather than
# its individual constituent packages).
#
# The Bioconductor packages used by the figures (ComplexHeatmap for the heatmap
# figures, plus ggtree/ggtreeExtra for the taxonomic tree, figure 1) are not on
# conda-forge but ARE available as precompiled binaries on the bioconda channel
# (built for R 4.5). They are installed as binaries, so no compiler toolchain or
# source compilation is needed.
BIOC_PACKAGES=(
  bioconductor-complexheatmap
  bioconductor-ggtree
  bioconductor-ggtreeextra
)
R_PACKAGES=(
  r-tidyverse
  r-glue=1.8.1
  r-rcolorbrewer=1.1_3
  r-dendextend=1.19.1
  r-patchwork=1.3.2
  r-circlize=0.4.18
  r-paletteer=1.7.0
  r-ggsci=5.2.0
  r-jcolors=0.0.5
  r-rstatix=1.1.0
  r-reshape2=1.4.5
  r-ggbreak=0.1.7
  r-plotly=4.12.1
  r-ggforce=0.5.0
  r-gplots=3.3.0
  r-jsonlite=2.0.0
  r-aricode=1.1.0
  r-ade4=1.7_24
  r-gridextra=2.3.1
  r-cluster=2.1.8.3
)
ensure_env plots jupyterlab=4.6.3 r-base=4.5.3 r-irkernel r-remotes r-biocmanager "${R_PACKAGES[@]}" -c conda-forge
# Register the R kernel of the `plots` env (points at envs/plots/bin/R)
conda run --no-capture-output -n plots Rscript -e 'IRkernel::installspec()'
# Install the Bioconductor R packages from bioconda as precompiled binaries
# (ComplexHeatmap, ggtree, ggtreeExtra). Idempotent: conda skips packages the
# env already has at the requested versions.
conda run --no-capture-output -n plots conda install -y -c conda-forge -c bioconda "${BIOC_PACKAGES[@]}"

ensure_env rdpg python=3.12
conda run --no-capture-output -n rdpg pip install -r ${CURRENT_DIR}/requirements_rdpg.txt

ensure_env embedding_comparator python=3.12
conda run --no-capture-output -n embedding_comparator pip install -r ${CURRENT_DIR}/requirements_embedding_comparator.txt
# Force numpy to the version required by the embedding-comparator tool
conda run --no-capture-output -n embedding_comparator pip install "numpy==2.0.0"
fi

echo "=== Installation complete ==="
