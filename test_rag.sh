#!/bin/bash
#SBATCH --job-name=ragdriver
#SBATCH --account=project_2010633
#SBATCH --partition=gpusmall
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:a100:1
## if local fast disk on a node is also needed, replace above line with:
#SBATCH --gres=gpu:a100:1,nvme:900
#

# export PATH="/projappl/project_2010633/Video-LLaVA/videollava_evn/bin:$PATH"

# export WORKSPACE=/projappl/project_2010633
export WORKSPACE=$(pwd)
export CACHESPACE=/scratch/project_2010633

export PATH=${WORKSPACE}/rag_env/bin:$PATH

export HF_DATASETS_CACHE=${CACHESPACE}/videollava_cache
export XDG_CACHE_HOME=${CACHESPACE}/videollava_cache
export PIP_CACHE_DIR=${CACHESPACE}/videollkava_cache
export TRANSFORMERS_CACHE=${CACHESPACE}/videollava_cache
export HF_HOME=${CACHESPACE}/videollava_cache

bash ${WORKSPACE}/scripts/finetune.sh