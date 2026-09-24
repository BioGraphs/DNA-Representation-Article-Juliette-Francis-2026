# Docker environment for the "Graph-based comparison..." paper

This directory defines a Docker image intended to **reproduce the repository's
conda environments** so you can run the RDPG/Jaccard pipelines and the
notebooks without installing conda/R on your host.

## Design: envs-only image + bind-mounted repo

The image installs **only the packages/environments**. The repo, its data and
its results are **not** baked in — they are **bind-mounted** over `/workspace`
at runtime. This means:

- The image is small and contains no data/submodules/Results.
- Your repo's `Data/` and `Results/` live on your host and **persist** across
  container runs (nothing is lost when the container is removed).
- On startup the entrypoint automatically runs `./install.sh --data-only`
  against the bind-mounted repo, unpacking `Data.tar.gz` and creating the
  `Results/` tree the first time. It is idempotent, so later starts are quick
  no-ops (set `AUTO_SETUP=0` to disable).

## Design notes

- **Bind-mount only — no network git fetch.** Submodules and `Data.tar.gz` come
  from your host repo via the bind mount, used as plain files by the pipelines;
  no network git fetch or private INRAE / SSH credentials are needed.
- **Bioconductor packages come from bioconda as precompiled binaries.**
  `ComplexHeatmap`, `ggtree`, and `ggtreeExtra` are not on conda-forge but are
  available on the bioconda channel, built for R 4.5. `install.sh --envs-only`
  installs them as binaries, so no compiler toolchain or source compilation is
  needed and the build stays fast.
- **The build sets up the environments only**; it does *not* unpack data, run
  the slow RDPG / Jaccard pipelines, or the notebooks (all of that happens at
  runtime against the bind-mounted repo).
- `install.sh` is idempotent and runs unmodified (with `--envs-only` at build,
  `--data-only` at runtime), so a change here tests the repo's own instructions.

## Prerequisites

- Docker (with build engine). Tested base: `ubuntu:26.04`, Miniconda latest.

## Build

Run from the repository root (the build context must be the repo root so that
`install.sh` and the two `requirements_*.txt` files are included):

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
- The image contains **no repo files** — a `docker run` without the bind mount
  will have neither the repo nor data (by design).

## Run — interactive shell (bind-mount the repo)

Mount the repository over `/workspace` so the entrypoint can set up `Data/` and
`Results/` on your host:

```bash
docker run --rm -it \
  -v "$PWD:/workspace" \
  dna-article:ubuntu26.04 bash
```

On the first run the entrypoint auto-unpacks `Data.tar.gz` and creates the
`Results/` tree in your host repo; later runs are no-ops. You land in
`/workspace` with conda initialised. Three envs are available:

| env                   | purpose                          |
|-----------------------|----------------------------------|
| `rdpg`                | RDPG comparison pipeline         |
| `embedding_comparator`| Jaccard-distance pipeline        |
| `plots`               | JupyterLab + R 4.5.3 (IRkernel)  |

Skip the automatic data setup by starting with `-e AUTO_SETUP=0`.

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

Results are written to `Results/` — because the repo is bind-mounted, they are
saved directly on your host.

> Figure 1 (taxonomic tree) uses `ggtree` / `ggtreeExtra`, and the heatmap
> figures use `ComplexHeatmap`. These Bioconductor packages are not on
> conda-forge, so `install.sh --envs-only` installs them into the `plots` env
> from the bioconda channel as precompiled binaries.

### Interactive JupyterLab

```bash
docker run --rm -it -p 8888:8888 \
  -v "$PWD:/workspace" \
  dna-article:ubuntu26.04 bash
conda activate plots
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then open the printed URL in your browser. Select the **R** kernel for the
notebooks.
