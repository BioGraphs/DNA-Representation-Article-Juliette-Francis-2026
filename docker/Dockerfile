# DNA Representation Article — reproducible environment
#
# Base image to (re)produce the environment for the
# "Graph-based comparison..." paper on a fresh machine.
# - OS : Ubuntu 26.04 LTS
# - CI : Miniconda (installed per the README instructions)
# - Envs: only the three conda environments are installed into the image
#         (rdpg, embedding_comparator, plots). The repo, data and results are
#         bind-mounted at runtime, so the image itself carries no repo files,
#         no Data.tar.gz and no Results/.
#
# Build (from the repo root so the build context includes the files we COPY):
#   docker build -t dna-article:ubuntu26.04 -f docker/Dockerfile .
#
# Run an interactive shell with the envs and the repo bind-mounted in:
#   docker run --rm -it -v "$PWD:/workspace" dna-article:ubuntu26.04
#
# See docker/README.md for details and the JupyterLab workflow.

FROM ubuntu:26.04

# ---------------------------------------------------------------------------
# System prerequisites (kept minimal; conda handles the Python/R toolchains and
# all R packages, including the Bioconductor ones from bioconda, are installed
# as precompiled binaries, so no compiler toolchain is required).
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
# Copy only the files needed to build the conda environments into the image.
# The repo, data and results are not part of the image: they are bind-mounted
# over /workspace at runtime. This keeps the context small and the image free
# of data/submodules/Results.
# The manifest files are copied before install.sh so changes to the repo
# alone do not bust the (slow) env-install layer cache.
# ---------------------------------------------------------------------------
WORKDIR /workspace
COPY install.sh requirements_rdpg.txt requirements_embedding_comparator.txt /opt/setup/

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
# Run the installer in envs-only mode: builds the three conda environments
# (rdpg, embedding_comparator, plots). No data unpack and no Results/ tree are
# created in the image — those happen at runtime against the bind-mounted repo.
# ---------------------------------------------------------------------------
RUN chmod +x /opt/setup/install.sh \
    && cd /opt/setup && bash ./install.sh --envs-only \
    # Register the plots env kernels (Python + IRkernel for R) so VS Code's
    # notebook kernel picker can find them inside the container.
    && conda run -n plots python -m ipykernel install --sys-prefix --name plots-python --display-name "Python (plots)" \
    && conda run -n plots Rscript -e 'IRkernel::installspec(name="plots-r", displayname="R (plots)", prefix="/opt/conda/envs/plots")'

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
