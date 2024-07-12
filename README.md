# RAG-Driver

The original repository is [here](https://github.com/YuanJianhao508/RAG-Driver); 

This repository only focus on implementing the program on cluster: [CSC](https://github.com/CSCfi)

## Project Structure



## Installation

```bash 
git clone https://github.com/timbrist/RAG-Driver.git
module load tykky
conda-containerize new --prefix ./rag_env rag_env.yml
```

After the installation, we need to add additional package.
The reason to do it sperately is because [tykky]() can not install ```pip install flash-attn --no-build-isolation ``` and can not use extra parameter to create new environment.

```bash 
module gcc/10.4.0 cuda/12.1.1 
conda-containerize update --post-install restpackages.sh ./rag_env
```

## Finetuning

```bash
sbatch run_rag.sh
tail -f slurm-*
```

Wait about 12 hours


