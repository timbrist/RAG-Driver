#!/bin/bash

# Set current diretory as workspace 
export WORKSPACE=$(pwd)

# Substitute the variables in the template file and create the final rag_env.yml
envsubst < environment.template.yml > rag_env.yml

# Create the conda environment
module load tykky
conda-containerize new --prefix ${WORKSPACE}/rag_env rag_env.yml 


