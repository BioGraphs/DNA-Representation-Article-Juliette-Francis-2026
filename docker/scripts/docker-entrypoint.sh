#!/bin/bash
# Entrypoint for the dna-representation-article image.
#
# Initialises conda (base + the three project envs stay available via
# `conda activate <name>`) and hands off to the requested command
# (default: an interactive bash shell in /workspace).
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
