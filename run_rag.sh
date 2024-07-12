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
export PATH="/projappl/project_2010633/RAG-Driver/rag_env/bin:$PATH"
export HF_DATASETS_CACHE=/scratch/project_2010633/videollava_cache
export XDG_CACHE_HOME=/scratch/project_2010633/videollava_cache
export PIP_CACHE_DIR=/scratch/project_2010633/videollkava_cache
export TRANSFORMERS_CACHE=/scratch/project_2010633/videollava_cache
export HF_HOME=/scratch/project_2010633/videollava_cache

bash ./scripts/finetune.sh