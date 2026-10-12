# 1. Create a virtual environment

Usefull documentation about [Bert model](https://huggingface.co/transformers/v3.0.2/model_doc/bert.html#bertmodel)

```bash
conda create --name dnaberts python=3.9
conda activate dnaberts
```

The file `requirements.txt` has been downloaded from [DNABERT-S GitHub page](https://github.com/MAGICS-LAB/DNABERT_S).
```bash
pip install -r ./representation_methods/DNABERT-S/requirements.txt
pip uninstall triton
```

## 2. Create the embedding

Open a terminal in the `dna_representation_article` directory and run the following command lines. It might take some time if you don't have a GPU (~1 hour).
```bash
conda activate dnaberts # if not already done
./representation_methods/DNABERT-S/dnaberts.sh
```