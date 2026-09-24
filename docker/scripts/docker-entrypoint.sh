#!/bin/bash
# Entrypoint for the dna-representation-article image.
#
# Initialises conda (base + the three project envs stay available via
# `conda activate <name>`) and hands off to the requested command
# (default: an interactive bash shell in /workspace).
#
# The image contains only the conda environments; the repo, data and results
# are bind-mounted at /workspace. On startup, unless AUTO_SETUP=0, we run
# `install.sh --data-only` to (re)create Data/ and Results/ against that
# bind-mounted repo. It is idempotent: when Data/Embeddings already exists it
# skips extraction, so re-runs are no-ops and nothing is re-unzipped.
set -e

# Make conda available to every interactive shell.
source "${CONDA_DIR}/etc/profile.d/conda.sh"

# shellcheck disable=SC1091
cat >> /etc/bash.bashrc <<'EOF'

# >>> conda initialize for all shells >>>
# The install happens in the entrypoint (layers are non-persistent anyway);
# this just makes the envs visible in interactive shells.
if [ -f /opt/conda/etc/profile.d/conda.sh ]; then
    . /opt/conda/etc/profile.d/conda.sh
    unset -f conda_base_func 2>/dev/null || true
fi
# <<< conda initialize <<<

EOF

cd /workspace

# ---------------------------------------------------------------------------
# Automatic host-side setup against the bind-mounted repo.
# Skips itself when /workspace/install.sh is absent (no bind mount / not the
# repo) or when AUTO_SETUP=0 is set. Safe to run on every start: install.sh's
# --data-only mode is idempotent.
# ---------------------------------------------------------------------------
if [ "${AUTO_SETUP:-1}" != "0" ] && [ -f /workspace/install.sh ]; then
    echo
    echo "=== Auto-setup: preparing Data/ and Results/ on the bind-mounted repo ==="
    bash /workspace/install.sh --data-only
fi

echo
echo "DNA-representation-article environment ready."
echo "Available conda envs (activate with 'conda activate <name>'):"
conda env list
echo
echo "  rdpg                 - RDPG comparison pipeline"
echo "  embedding_comparator - Jaccard-distance pipeline"
echo "  plots                - notebook analysis (JupyterLab + R kernel)"
echo
echo "Work-in-progress pipelines and notebooks run from /workspace."
echo "See /workspace/README.md for the exact commands."
echo

exec "$@"
