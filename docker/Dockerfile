# DNA Representation Article — reproducible environment
#
# Base image to (re)produce the environment for the
# "Graph-based comparison..." paper on a fresh machine.
# - OS : Ubuntu 26.04 LTS
# - CI : Miniconda (installed per the README instructions)
# - Repo: the current workspace is COPYed in, submodules checked out,
#         and `install.sh` is run to build the three conda envs and data.
#
# Build (from the repo root so the build context includes it):
#   docker build -t dna-article:ubuntu26.04 -f docker/Dockerfile .
#
# Run an interactive shell with the envs and repo:
#   docker run --rm -it dna-article:ubuntu26.04
#
# See docker/README.md for details and the JupyterLab workflow.

FROM ubuntu:26.04

# ---------------------------------------------------------------------------
# System prerequisites (kept minimal; conda handles the Python/R toolchains).
# ---------------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Miniconda (mirrors the README step "install conda if you do not have it").
# Installed into /opt/conda and activated for all subsequent RUN layers.
# ---------------------------------------------------------------------------
ENV MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
ENV CONDA_DIR=/opt/conda
ENV PATH=${CONDA_DIR}/bin:${PATH}
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN curl -fsSL -o /tmp/miniconda.sh "${MINICONDA_URL}" \
    && bash /tmp/miniconda.sh -b -p "${CONDA_DIR}" \
    && rm -f /tmp/miniconda.sh \
    && conda config --set always_yes yes \
    && conda config --set auto_activate_base false \
    && conda --version \
    # Accept the Anaconda Terms of Service for the default commercial
    # channels; required by recent conda (>=26) before any solve can run.
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# ---------------------------------------------------------------------------
# Copy the repository (source files + Data.tar.gz + the checked-out submodule
# working trees) into the image.
# .dockerignore excludes the local gitignored Data/ and Results/ so the fresh
# install.sh flow (unpack Data.tar.gz, create Results/) is exercised exactly as
# it would be on a new machine.
#
# The submodules (embedding-comparator, dna2vec, hyena-dna, ...) are already
# checked out in the build context and are used as plain files by the
# pipelines, so they are copied verbatim; no network git fetch is needed and
# the private INRAE remote / SSH keys are never required inside the build.
# ---------------------------------------------------------------------------
WORKDIR /workspace
COPY . /workspace/

# ---------------------------------------------------------------------------
# Make `pip install` resilient to flaky networks when the envs are built.
# install.sh calls `pip install -r requirements_*.txt` (via `conda run`), which
# honours these env vars. Without this, a large torch/CUDA wheel download that
# keeps getting interrupted can exhaust pip's 6-attempt resume limit and abort
# the whole build.
# ---------------------------------------------------------------------------
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_RETRIES=15

# ---------------------------------------------------------------------------
# Run the (idempotent) installer.
# This unpacks Data.tar.gz, creates the Results/ tree, and builds the three
# conda environments: rdpg, embedding_comparator, plots.
# ---------------------------------------------------------------------------
RUN chmod +x install.sh \
    && bash ./install.sh

# Copy the interactive entrypoint / helper scripts.
COPY docker/scripts /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/run-notebooks.sh

# ---------------------------------------------------------------------------
# Runtime: start an interactive shell with conda available so the user can
# activate any of the envs and run the (slow) pipelines/notebooks manually.
# ---------------------------------------------------------------------------
WORKDIR /workspace

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["bash"]
