#!/bin/bash
# Run a notebook headlessly in the `plots` env to verify the analysis stack.
#
# Usage:
#   run-notebooks.sh [nb1.ipynb ...]
#
# With no arguments, all `plots/*.ipynb` are executed. Output goes to a
# dedicated out-dir so the repo's own notebooks are never overwritten.
set -e

NB_DIR=/workspace/plots
OUT_DIR=/workspace/Results/Plots/notebook_execution
mkdir -p "${OUT_DIR}"

if [ "$#" -eq 0 ]; then
    notebooks=("${NB_DIR}"/*.ipynb)
else
    notebooks=("$@")
fi

for nb in "${notebooks[@]}"; do
    name="$(basename "${nb}" .ipynb)"
    echo "=== Executing ${name}.ipynb ==="
    conda run --no-capture-output -n plots jupyter nbconvert \
        --to notebook \
        --execute \
        --inplace=false \
        --output "${OUT_DIR}/${name}_executed.ipynb" \
        "${nb}"
done

echo
echo "All notebooks executed. Outputs in: ${OUT_DIR}"
