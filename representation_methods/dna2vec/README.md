# 1. Create a virtual environment

```bash
conda create --name dna2vec python=3.6
conda activate dna2vec
pip3 install -r dna2vec/requirements.txt
```
There are warnings during the packages installation that do not have an impact on the embedding making.


## 2. Create the embedding

Open a terminal in the dna_representation_article directory and run the following command lines.
```bash
conda activate dna2vec # if not already done
./representation_methods/dna2vec/DNA2VEC.sh
```