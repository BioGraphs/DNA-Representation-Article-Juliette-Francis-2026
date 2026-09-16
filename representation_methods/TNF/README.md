This directory contains scripts to use Tetra-Nucleotide Frequency (TNF) on the bacteria_1 dataset.

# 1. Create a virtual environment with desired packages

```bash
conda create --name TNF python=3.10 pandas scikit-learn
conda activate TNF
```

## 2. Create the representation

Open a terminal in the dna_representation_article directory and run the following command lines.
```bash
conda activate TNF
./representation_methods/TNF/TNF.sh
```