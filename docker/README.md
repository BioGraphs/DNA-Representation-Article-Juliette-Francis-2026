# Docker environment for the "Graph-based comparison..." paper

This directory defines a Docker image intended to **reproduce the repository's
environment on a fresh machine** and let you verify that the notebooks run and
the results can be regenerated.

The image is based on **Ubuntu 26.04 LTS**, installs **Miniconda** (as the
README instructs), copies the repository (source + `Data.tar.gz` + the checked
out submodules), and runs `install.sh` to build the three conda environments
(`rdpg`, `embedding_comparator`, `plots`) and unpack the data.

## Design notes

- **No SSH/INRAE credentials needed.** The repo is copied from your local
  workspace into the image. The submodules are copied verbatim as plain files
  (the pipelines use them as files), so there is no network git fetch during the
  build. Only Miniconda and the conda-forge/pip artifacts are downloaded.
- **`Data/` and `Results/` are excluded by `.dockerignore`.** They are recreated
  from `Data.tar.gz` / `install.sh` inside the container, matching the
  new-machine flow exactly. This also keeps the build context small.
- **The build sets up the environments only**; it does *not* run the slow RDPG /
  Jaccard pipelines or the notebooks (those can be run interactively afterwards).
- `install.sh` is idempotent and runs unmodified, so a change here tests the
  repo's own instructions.

## Prerequisites

- Docker (with build engine). Tested base: `ubuntu:26.04`, Miniconda latest.

## Build

Run from the repository root (the build context must be the repo root so that
`Data.tar.gz` and the submodules are included):

```bash
cd dna_representation_article

docker build -t dna-article:ubuntu26.04 -f docker/Dockerfile .
```

Notes:
- Building the `rdpg` env downloads PyTorch and the other pip/conda packages, so
  the first build can take a while. Subsequent builds reuse the layer cache
  unless the requirements change.
- If `docker build` needs more memory than defaults allow (PyTorch install /
  conda solve), pass `--memory`/`--memory-swap` to the docker daemon as needed.

## Run — interactive shell

```bash
docker run --rm -it dna-article:ubuntu26.04 bash
```

You land in `/workspace` with conda initialised. Three envs are available:

| env                   | purpose                          |
|-----------------------|----------------------------------|
| `rdpg`                | RDPG comparison pipeline         |
| `embedding_comparator`| Jaccard-distance pipeline        |
| `plots`               | JupyterLab + R 4.4.3 (IRkernel)  |

## Reproduce results inside the container

From within the container (`cd /workspace`):

```bash
# RDPG pipeline
conda activate rdpg
./rdpg/compare_emb_with_rdpg.sh

# Jaccard pipeline (strict order, embedding_comparator env)
conda activate embedding_comparator
python3 ./jaccard_distance/prepare_data.py ./jaccard_distance/embedding_paths.txt
./jaccard_distance/preprocess_data.sh
./jaccard_distance/jaccard_similarity.sh
```

### Run a notebook headlessly (verifies the R stack end-to-end)

A helper is bundled in the image:

```bash
run-notebooks.sh                    # execute every plots/*.ipynb
run-notebooks.sh plots/pca_projection_figure_2.ipynb   # a single notebook
```

Executed copies are written to `Results/Plots/notebook_execution/` so the
repo's own notebooks are never modified.

> Figure 1 (taxonomic tree) additionally needs `ggtree` / `ggtreeExtra`, which
> are intentionally **not** installed by `install.sh` (not on conda-forge; see
> README). Install them separately if you need figure 1.

### Interactive JupyterLab

```bash
docker run --rm -it -p 8888:8888 dna-article:ubuntu26.04 bash
conda activate plots
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then open the printed URL in your browser. Select the **R** kernel for the
notebooks.
