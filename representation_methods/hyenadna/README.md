# 1. Set up environment

Please download [weights.ckpt](https://huggingface.co/LongSafari/hyenadna-small-32k-seqlen/tree/main) and replace the weight.ckpt from the `hyenadna-small-32k-seqlen` repository by the one you just downloaded.

Please install [apptainer](https://apptainer.org/docs/admin/main/installation.html#install-from-pre-built-packages).

Open a terminal in the directory `dna_representation_article/representation_methods/HyenaDNA` and run the following command line:
```bash
apptainer pull docker://hyenadna/hyena-dna:latest
```

## 2. Create the embedding

Still in the directory `dna_representation_article/representation_methods/HyenaDNA`, run the following command line:
```bash
./hyenadna.sh
```