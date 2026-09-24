#!/bin/bash
# Launch JupyterLab for the dna-article workspace.
#
# - Runs from the `plots` env (has JupyterLab + R IRkernel + Python kernel).
# - Binds 0.0.0.0:8888 so it works from inside the devcontainer port-forward.
# - --allow-root / --no-browser silence the root warning and don't open a browser.
# - A fixed token keeps the URL stable/prefillable ("dna").
#
# Usage:  jupyterlab-start.sh   (kept running in the foreground)
set -e

PORT="${JUPYTER_PORT:-8888}"
TOKEN="${JUPYTER_TOKEN:-dna}"

echo
echo "Starting JupyterLab (plots env) on port ${PORT} ..."
echo "URL:   http://localhost:${PORT}/?token=${TOKEN}"
echo "(also reachable at VS Code's 'PORTS' panel if forwarded)"
echo

exec /opt/conda/envs/plots/bin/jupyter lab \
    --ip=0.0.0.0 \
    --port="${PORT}" \
    --no-browser \
    --allow-root \
    --notebook-dir=/workspace \
    --ServerApp.token="${TOKEN}" \
    --ServerApp.password=""
