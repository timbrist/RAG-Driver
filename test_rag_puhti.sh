#!/bin/bash
#SBATCH --job-name=ragdriver
#SBATCH --account=<project>
#SBATCH --partition=gpu
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=8000
#SBATCH --gres=gpu:v100:1

# export WORKSPACE=/projappl/project_2010633
export WORKSPACE=$(pwd)

export CACHESPACE=$(pwd)/cache

export PATH=${WORKSPACE}/rag_env/bin:$PATH
export HF_DATASETS_CACHE=${CACHESPACE}
export XDG_CACHE_HOME=${CACHESPACE}
export PIP_CACHE_DIR=${CACHESPACE}
export TRANSFORMERS_CACHE=${CACHESPACE}
export HF_HOME=${CACHESPACE}

bash ${WORKSPACE}/scripts/finetune.sh