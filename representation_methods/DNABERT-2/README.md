# 1. Create a virtual environment

Usefull documentation about [Bert model](https://huggingface.co/transformers/v3.0.2/model_doc/bert.html#bertmodel)

```bash
conda create --name dnabert2 python=3.8
conda activate dnabert2
```

The file `requirements.txt` has been downloaded from [DNABERT-2 GitHub page](https://github.com/MAGICS-LAB/DNABERT_2).
```bash
pip install -r ./representation_methods/DNABERT-2/requirements.txt
pip uninstall triton
```

## 3. Create the embedding (GPU Nvidia needed)

Open a terminal in the `dna_representation_article` directory and run the following command lines.
```bash
conda activate dnabert2 # if not already done
./representation_methods/DNABERT-2/dnabert2.sh
```
