#!/bin/bash

# Set current diretory as workspace 
export WORKSPACE=$(pwd)

# Substitute the variables in the template file and create the final rag_env.yml
envsubst < environment.template.yml > rag_env.yml

# Create the conda environment
module load tykky
conda-containerize new --prefix ${WORKSPACE}/rag_env rag_env.yml 


# install the rest of the packages 
module gcc/10.4.0 cuda/12.1.1 
conda-containerize update --post-install ${WORKSPACE}/restpackages.sh ${WORKSPACE}/rag_env


