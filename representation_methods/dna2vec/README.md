# 1. Create a virtual environment

```bash
conda create --name dna2vec python=3.6
conda activate dna2vec
```

# 2. Installation

```bash
git submodule add https://github.com/pnpnpn/dna2vec.git
git commit -am 'Add dna2vec module'
git push
pip3 install -r dna2vec/requirements.txt
```

Warning when installing requirements

```bash
(dna2vec) [~/scratch/DNA_embedding/dna2vec]$ pip install -r requirements.txt
Collecting arrow==0.8.0
  Using cached arrow-0.8.0.tar.gz (81 kB)
  Preparing metadata (setup.py) ... done
Collecting biopython==1.68
  Using cached biopython-1.68.tar.gz (14.4 MB)
  Preparing metadata (setup.py) ... done
Collecting boto==2.46.1
  Using cached boto-2.46.1-py2.py3-none-any.whl (1.4 MB)
Collecting bz2file==0.98
  Using cached bz2file-0.98.tar.gz (11 kB)
  Preparing metadata (setup.py) ... done
Collecting ConfigArgParse==0.11.0
  Using cached ConfigArgParse-0.11.0.tar.gz (40 kB)
  Preparing metadata (setup.py) ... done
Collecting gensim==0.13.2
  Using cached gensim-0.13.2.tar.gz (6.4 MB)
  Preparing metadata (setup.py) ... done
Collecting Logbook==1.0.0
  Using cached Logbook-1.0.0.tar.gz (178 kB)
  Preparing metadata (setup.py) ... done
Collecting numpy==1.16
  Downloading numpy-1.16.0-cp36-cp36m-manylinux1_x86_64.whl (17.3 MB)
     |████████████████████████████████| 17.3 MB 3.6 MB/s            
Collecting pep8==1.7.0
  Downloading pep8-1.7.0-py2.py3-none-any.whl (41 kB)
     |████████████████████████████████| 41 kB 44 kB/s              
Collecting pluggy==0.4.0
  Downloading pluggy-0.4.0-py2.py3-none-any.whl (11 kB)
Collecting py==1.4.33
  Downloading py-1.4.33-py2.py3-none-any.whl (83 kB)
     |████████████████████████████████| 83 kB 748 kB/s             
Collecting pytest==3.0.7
  Downloading pytest-3.0.7-py2.py3-none-any.whl (172 kB)
     |████████████████████████████████| 172 kB 50.0 MB/s            
Collecting python-dateutil==2.6.0
  Downloading python_dateutil-2.6.0-py2.py3-none-any.whl (194 kB)
     |████████████████████████████████| 194 kB 45.1 MB/s            
Collecting requests==2.20.0
  Downloading requests-2.20.0-py2.py3-none-any.whl (60 kB)
     |████████████████████████████████| 60 kB 1.1 MB/s             
Collecting scipy==0.19.0
  Downloading scipy-0.19.0-cp36-cp36m-manylinux1_x86_64.whl (48.2 MB)
     |████████████████████████████████| 48.2 MB 158 kB/s             
Collecting six==1.10.0
  Downloading six-1.10.0-py2.py3-none-any.whl (10 kB)
Collecting smart-open==1.5.1
  Downloading smart_open-1.5.1.tar.gz (27 kB)
  Preparing metadata (setup.py) ... done
Collecting tox==2.7.0
  Downloading tox-2.7.0-py2.py3-none-any.whl (49 kB)
     |████████████████████████████████| 49 kB 2.0 MB/s             
Collecting tox-pyenv==1.0.3
  Downloading tox_pyenv-1.0.3-py2.py3-none-any.whl (6.1 kB)
Collecting virtualenv==15.1.0
  Downloading virtualenv-15.1.0-py2.py3-none-any.whl (1.8 MB)
     |████████████████████████████████| 1.8 MB 49.1 MB/s            
Requirement already satisfied: setuptools in /home/genouest/cnrs_umr6074/jfrancis/.conda/envs/dna2vec/lib/python3.6/site-packages (from pytest==3.0.7->-r requirements.txt (line 12)) (58.0.4)
Collecting chardet<3.1.0,>=3.0.2
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
     |████████████████████████████████| 133 kB 57.2 MB/s            
Collecting certifi>=2017.4.17
  Downloading certifi-2024.8.30-py3-none-any.whl (167 kB)
     |████████████████████████████████| 167 kB 53.0 MB/s            
Collecting idna<2.8,>=2.5
  Downloading idna-2.7-py2.py3-none-any.whl (58 kB)
     |████████████████████████████████| 58 kB 3.4 MB/s             
Collecting urllib3<1.25,>=1.21.1
  Downloading urllib3-1.24.3-py2.py3-none-any.whl (118 kB)
     |████████████████████████████████| 118 kB 53.9 MB/s            
Building wheels for collected packages: arrow, biopython, bz2file, ConfigArgParse, gensim, Logbook, smart-open
  Building wheel for arrow (setup.py) ... done
  Created wheel for arrow: filename=arrow-0.8.0-py3-none-any.whl size=31310 sha256=3c8126cd3fe8759dc05d35e270f5a03bf01e1323c0c4ee89eb044f04f67b6162
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/2f/a4/0f/c621ee9ed356f048e6d2f083ef7fedbbfe4ede961d782435e6
  Building wheel for biopython (setup.py) ... error
  ERROR: Command errored out with exit status 255:
   command: /home/genouest/cnrs_umr6074/jfrancis/.conda/envs/dna2vec/bin/python3.6 -u -c 'import io, os, sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-687xd00l/biopython_3ab53323d1be49498fc436e86e807c83/setup.py'"'"'; __file__='"'"'/tmp/pip-install-687xd00l/biopython_3ab53323d1be49498fc436e86e807c83/setup.py'"'"';f = getattr(tokenize, '"'"'open'"'"', open)(__file__) if os.path.exists(__file__) else io.StringIO('"'"'from setuptools import setup; setup()'"'"');code = f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-tmcs4ahv
       cwd: /tmp/pip-install-687xd00l/biopython_3ab53323d1be49498fc436e86e807c83/
  Complete output (13 lines):
  running bdist_wheel
  running build
  running build_py
  
  Numerical Python (NumPy) is not installed.
  
  This package is required for many Biopython features.  Please install
  it before you install Biopython. You can install Biopython anyway, but
  anything dependent on NumPy will not work. If you do this, and later
  install NumPy, you should then re-install Biopython.
  
  You can find NumPy at http://www.numpy.org
  
  ----------------------------------------
  ERROR: Failed building wheel for biopython
  Running setup.py clean for biopython
  Building wheel for bz2file (setup.py) ... done
  Created wheel for bz2file: filename=bz2file-0.98-py3-none-any.whl size=6882 sha256=35722d37556535b318546dce88639b477fbbe2b25a9a7dabd03f2468087a94ac
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/4b/91/8e/36cb51df0557cdcc7c546253681ae08da161830677da4020f7
  Building wheel for ConfigArgParse (setup.py) ... done
  Created wheel for ConfigArgParse: filename=ConfigArgParse-0.11.0-py3-none-any.whl size=17811 sha256=131baa54f206e12a55c7a09bf5f8347b316ff65b85a7f29b8e826f3ae232faef
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/1e/65/ee/20e213751308b1d63cb4c1b535a4fa7a1ff3a56e2f045b380f
  Building wheel for gensim (setup.py) ... done
  Created wheel for gensim: filename=gensim-0.13.2-cp36-cp36m-linux_x86_64.whl size=4469781 sha256=4c4cdc20ab48ab96fa5aba5bc141df58e68442cb4696e1fb8cc814d1b41a85b9
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/0c/78/e0/c1a5a927ae58b4d211eb94378565a23595b715edd4182085fb
  Building wheel for Logbook (setup.py) ... done
  Created wheel for Logbook: filename=Logbook-1.0.0-cp36-cp36m-linux_x86_64.whl size=208969 sha256=85e1b815638754bc6e44b7ceff86b4462eaeb3cda88dbfc1bb688748dcd535cf
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/e6/68/1d/56b9cb003f4b5e685d55a5b6990b6d628b809c0db343636cb0
  Building wheel for smart-open (setup.py) ... done
  Created wheel for smart-open: filename=smart_open-1.5.1-py3-none-any.whl size=28611 sha256=27fda2bc1419717142011b328d7a20cbb0925e0b6093ff3666b480a504aa7260
  Stored in directory: /home/genouest/cnrs_umr6074/jfrancis/.cache/pip/wheels/c7/cd/27/c86760bff71b21464d69b0397df95050f3343367b5abe61d17
Successfully built arrow bz2file ConfigArgParse gensim Logbook smart-open
Failed to build biopython
Installing collected packages: urllib3, idna, chardet, certifi, virtualenv, six, requests, py, pluggy, numpy, bz2file, boto, tox, smart-open, scipy, python-dateutil, tox-pyenv, pytest, pep8, Logbook, gensim, ConfigArgParse, biopython, arrow
    Running setup.py install for biopython ... done
  DEPRECATION: biopython was installed using the legacy 'setup.py install' method, because a wheel could not be built for it. A possible replacement is to fix the wheel build issue reported above. Discussion can be found at https://github.com/pypa/pip/issues/8368
Successfully installed ConfigArgParse-0.11.0 Logbook-1.0.0 arrow-0.8.0 biopython-1.68 boto-2.46.1 bz2file-0.98 certifi-2024.8.30 chardet-3.0.4 gensim-0.13.2 idna-2.7 numpy-1.16.0 pep8-1.7.0 pluggy-0.4.0 py-1.4.33 pytest-3.0.7 python-dateutil-2.6.0 requests-2.20.0 scipy-0.19.0 six-1.10.0 smart-open-1.5.1 tox-2.7.0 tox-pyenv-1.0.3 urllib3-1.24.3 virtualenv-15.1.0

```

Test the installation:
```bash
python3 ./dna2vec/scripts/train_dna2vec.py -c ./dna2vec/configs/small_example.yml
```
Error linked to the version of the package Gensim
```bash
Traceback (most recent call last):
  File "./scripts/train_dna2vec.py", line 142, in <module>
    main()
  File "./scripts/train_dna2vec.py", line 139, in main
    run_main(args, inputs, out_fileroot)
  File "./scripts/train_dna2vec.py", line 88, in run_main
    learner.write_vec()
  File "./scripts/train_dna2vec.py", line 55, in write_vec
    self.model.wv.save_word2vec_format(out_filename, binary=False)
AttributeError: 'Word2Vec' object has no attribute 'wv'
```

In newer versions of gensim (>=4.0.0), the Word2Vec model's vocabulary and vectors are stored in model.wv.
In older versions (<4.0.0), you should access vectors directly as model instead of model.wv.
But the requierements file requieres gensim==0.13.2.
It seems that it does not have an impact on the embedding making.

# 3. Init the submodule when the main repository is cloned

```bash
git clone git@forgemia.inra.fr:holobionts_pepr/workpackage_1/phd_juliette_francis.git
git submodule init
git submodule update
```

## 4. Create embedding

Run dna2vec.sh file.