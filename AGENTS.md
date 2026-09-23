# AGENTS.md

Code to reproduce the results of the "Graph-based comparison..." paper. It compares DNA sequence representations (TNF, dna2vec, HyenaDNA, DNABERT-2, DNABERT-S) via Jaccard distance and RDPG.

## Repo layout
- `jaccard_distance/` — Jaccard-distance comparison pipeline (depends on the `embedding-comparator` submodule).
- `rdpg/` — RDPG comparison pipeline (5 sequential python steps, driven by `compare_emb_with_rdpg.sh`).
- `plots/` — Jupyter notebooks that generate each article figure (R + Python).
- `representation_methods/<METHOD>/` — optional scripts to regenerate embeddings (not needed to reproduce results; outputs get `_bis` suffix so originals aren't overwritten).

## Setup (all conda-based, no root dependency manifests)
1. `git submodule update --init --recursive` — required; several submodules (embedding-comparator, dna2vec, hyena-dna, and a HuggingFace model repo).
2. `./install.sh` — unpacks `Data.tar.gz` and creates `Results/`. It creates three conda envs — `rdpg`, `embedding_comparator`, `plots` — from the `requirements_*.txt` files at the repo root.

`install.sh` is **idempotent**: re-running is safe (skips extracting `Data` and `conda create` if already present, uses `mkdir -p`).

Gotchas:
- `Data/` and `Results/` are **gitignored** and produced locally; they are not tracked. Do not commit them.
- The three envs are defined by `requirements_rdpg.txt`, `requirements_embedding_comparator.txt`, `requirements_plots.txt` at the repo root. To re-create an env manually: `conda create -n <name> python=3.12 && pip install -r requirements_<name>.txt`.
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

## Gotchas
- Figure S6 (`k_value_exploration_figure_S6.ipynb`) needs multiple RDPG runs with different `K` values (5, 10, 25, 40, 55, 70). `compare_emb_with_rdpg.sh` runs only one `K` per invocation — edit the `K=` line at the top and re-run per value. The default is `K=25`.
- Scripts are run from the repo root (`$PWD`-relative paths in `.sh` files).
- RDPG/HyenaDNA pipelines are slow; DNABERT-S inference is slow without a GPU.
