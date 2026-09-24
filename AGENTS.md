# AGENTS.md

Code to reproduce the results of the "Graph-based comparison..." paper. It compares DNA sequence representations (TNF, dna2vec, HyenaDNA, DNABERT-2, DNABERT-S) via Jaccard distance and RDPG.

## Repo layout
- `jaccard_distance/` — Jaccard-distance comparison pipeline (depends on the `embedding-comparator` submodule).
- `rdpg/` — RDPG comparison pipeline (5 sequential python steps, driven by `compare_emb_with_rdpg.sh`).
- `plots/` — Jupyter notebooks that generate each article figure (R + Python).
- `representation_methods/<METHOD>/` — optional scripts to regenerate embeddings (not needed to reproduce results; outputs get `_bis` suffix so originals aren't overwritten).
- `docker/` — Docker image (Ubuntu 26.04 + Miniconda + the three envs) to reproduce the environment on a fresh machine. See `docker/README.md` for full details.

## Setup (all conda-based, no root dependency manifests)
1. `git submodule update --init --recursive` — required; several submodules (embedding-comparator, dna2vec, hyena-dna, and a HuggingFace model repo).
2. `./install.sh` — unpacks `Data.tar.gz` and creates `Results/`. It creates three conda envs — `rdpg`, `embedding_comparator`, `plots`.

`install.sh` is **idempotent**: re-running is safe (skips extracting `Data` and `conda create` if already present, uses `mkdir -p`).

Gotchas:
- `Data/` and `Results/` are **gitignored** and produced locally; they are not tracked. Do not commit them.
- `rdpg` and `embedding_comparator` are defined by `requirements_rdpg.txt` and `requirements_embedding_comparator.txt` at the repo root; re-create manually with `conda create -n <name> python=3.12 && pip install -r requirements_<name>.txt`. The `plots` env has **no** requirements file — `install.sh` installs all its R/conda packages itself (pinned R 4.5.3 + IRkernel, registered via `IRkernel::installspec()`).
- `embedding_comparator` needs `numpy==2.0.0` pinned (later versions break the embedding-comparator tool); `install.sh` forces it after installing requirements.
- Work with data from `Data/Embeddings/`, e.g. `bacteria_1_tnf_embedding.csv`; one row per sequence, comma-separated.

## Commands (run the pipeline in order)
RDPG:
```bash
conda activate rdpg
./rdpg/compare_emb_with_rdpg.sh
```
Jaccard (note: strict order, must be in the `embedding_comparator` env):
```bash
conda activate embedding_comparator
python3 ./jaccard_distance/prepare_data.py ./jaccard_distance/embedding_paths.txt
./jaccard_distance/preprocess_data.sh
./jaccard_distance/jaccard_similarity.sh
```

Notebooks (`plots/*.ipynb`) need the `plots` env and an IRkernel (R) installed. Run the RDPG/Jaccard pipelines **before** running notebooks; they read `Results/`.

## Docker (reproduce the environment on a fresh machine)
The `docker/` directory builds Ubuntu 26.04 + Miniconda + all three conda envs, reproducing the setup on a machine with no conda/R install. Full details: `docker/README.md`.

Key design points:
- **Envs-only image + bind-mounted repo.** The build installs only the three conda envs (`install.sh --envs-only`); the repo, `Data.tar.gz`, submodules and `Results/` are **not** in the image — they come from a host bind mount over `/workspace`.
- **Build context is minimal.** Only `install.sh` + `requirements_*.txt` + `docker/scripts` are `COPY`ed into the image; there is no `COPY .`. `Data.tar.gz`/submodules are never baked in.
- **Auto data setup at runtime.** `docker-entrypoint.sh` runs `install.sh --data-only` on start against the bind-mounted repo (idempotent: skips unpack once `Data/Embeddings` exists). Disable with `-e AUTO_SETUP=0`. Data/Results persist on the host.
- **No SSH/INRAE creds / no network git fetch** — submodules come from the host mount as plain files.
- The Dockerfile appends `PIP_RETRIES`/`PIP_DEFAULT_TIMEOUT` and accepts the Miniconda Anaconda ToS so installs survive flaky networks.

Build (context must be repo root) and run (**bind mount required**):
```bash
docker build -t dna-article:ubuntu26.04 -f docker/Dockerfile .
docker run --rm -it -v "$PWD:/workspace" dna-article:ubuntu26.04 bash   # lands in /workspace; auto-setups Data/Results on the host
```
Inside the container the same env names and pipeline commands apply as above. `Results/` written by the pipelines are saved to the host via the bind mount. A `run-notebooks.sh` helper executes `plots/*.ipynb` headlessly (output to `Results/Plots/notebook_execution/`, originals untouched). Note `run-notebooks.sh` path is hardcoded to `/workspace/plots` — container-only, not portable to host.

Gotchas (Docker):
- Keep the build context at the repo root so `install.sh` + `requirements_*.txt` are included.
- `rdpg` env build downloads PyTorch/CUDA — first build is slow; the tiny build context keeps it as small as possible.
- `install.sh --envs-only` (build-time) creates only envs; `--data-only` (runtime) only unpacks data + creates `Results/`; the no-arg form does both (manual conda flow).
- The Bioconductor R packages used by the figures — `ComplexHeatmap` (heatmaps) and `ggtree`/`ggtreeExtra` (figure 1) — are **not on conda-forge** but ARE installed into the `plots` env from **bioconda** as precompiled R 4.5 binaries (no compiler toolchain needed). If (re)building envs by hand, use `-c conda-forge -c bioconda`.

## Gotchas
- Figure S6 (`k_value_exploration_figure_S6.ipynb`) needs multiple RDPG runs with different `K` values (5, 10, 25, 40, 55, 70). `compare_emb_with_rdpg.sh` runs only one `K` per invocation — edit the `K=` line at the top and re-run per value. The default is `K=25`.
- Scripts are run from the repo root (`$PWD`-relative paths in `.sh` files).
- RDPG/HyenaDNA pipelines are slow; DNABERT-S inference is slow without a GPU.
