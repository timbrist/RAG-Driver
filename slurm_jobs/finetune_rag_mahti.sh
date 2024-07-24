#!/bin/bash
#SBATCH --job-name=ragdriver
#SBATCH --account=project_2010633
#SBATCH --partition=gpumedium
#SBATCH --time=15:00:00
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:a100:4

# export PATH="/projappl/project_2010633/Video-LLaVA/videollava_evn/bin:$PATH"
export WORKSPACE=$(pwd)

export CACHESPACE=/scratch/project_2010633/videollava_cache

export PATH=${WORKSPACE}/rag_env/bin:$PATH
export HF_DATASETS_CACHE=${CACHESPACE}
export XDG_CACHE_HOME=${CACHESPACE}
export PIP_CACHE_DIR=${CACHESPACE}
export TRANSFORMERS_CACHE=${CACHESPACE}
export HF_HOME=${CACHESPACE}


bash ${WORKSPACE}/scripts/finetune.sh