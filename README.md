# RAG-Driver

The original repository is [here](https://github.com/YuanJianhao508/RAG-Driver); 
Thank [YuanJianhao508](https://github.com/YuanJianhao508) for doing such amazing work.

This repository only focus on implementing the program on cluster: [CSC](https://github.com/CSCfi)


## Project Structure

- `/RAG-DRIVER`   
  - `/llava`          - [videollava](https://github.com/PKU-YuanGroup/Video-LLaVA)
  - `/models`         - This folder contains checkpoint models from [LangugeBind](https://huggingface.co/LanguageBind).
    - `/LanguageBind_Image`         - [download from huggingface](https://huggingface.co/LanguageBind/LanguageBind_Image).
    - `/LanguageBind_Video_merge`   - [download from huggingface](https://huggingface.co/LanguageBind/LanguageBind_Video_merge).
    - `/Video-LLaVA-7B`             - [download from huggingface](https://huggingface.co/LanguageBind/Video-LLaVA-7B).
    - `/Video-LLaVA-Pretrain-7B`    - [download from huggingface](https://huggingface.co/LanguageBind/Video-LLaVA-Pretrain-7B).
  - `/rag_env`         - RAG-Driver virtual environment for containerization  
  - `README.md`     - Overview and general information about the project.
  - `.gitignore`    - Specifies patterns of files to ignore in Git operations.

## Installation


**NOTE**: The virtual environment require load 2 modules: tykky and cuda. 
```bash 
git clone https://github.com/timbrist/RAG-Driver.git
cd RAG-Driver # we will continue use this folder as WORKSPACE, This will be the only change directory of all.
export CW_DEBUG_KEEP_FILES=${pwd}
bash create_rag_env.sh
```

After the installation, we need to add additional package.
The reason to do it sperately is because [tykky](https://docs.csc.fi/computing/containers/tykky/) can not install ```pip install flash-attn --no-build-isolation ``` and can not use extra parameter to create new environment.

Please check the **create_rag_env.sh** file to make sure the version of cuda is above 11.7

```bash 
module spider cuda #use this to check which cuda your system support, use cuda/11.7+ please.
module cuda 
conda-containerize update --post-install restpackages.sh ./rag_env
```


## Data Preparation


### Download checkpoint models

This step is for people who cannot use git lfs to download files from hugginface. 
This script will automatically download the checkpoint models.

**NOTE**: The checkpoint models will take up at least: 46GB. 
If you don't have much space in current directory, please change **MODELS_DIR** in download.sh to desired diretory:
export MODELS_DIR=path/to/models. In this case, you will have to specify your model path in scripts/finetune.sh too.

```bash
bash download.sh
```

### Download processed BDD-X dataset 

Processed Version of BDD-X is available from [here](https://drive.google.com/file/d/14a3QTkWRelAZs-kW_2U5tjYcAm2l8VbF/view)

**If you want to download the dataset manually, Please unzip the file into video_process folder**

Then run the following command: 
```bash
bash get_bddx_dataset.sh
```

## Usage 

Cannot find a way to automate the process. 
A lot of things need to config in this step.

**NOTE**: Please remember to change:  \
MODELS_DIR in scripts/finetune.sh 
CACHESPACE in run_rag.sh and test_rag.sh
```--account=<project> ``` specify your project name such as project_2010795

the script is follow the exmaple on [Puhti](https://docs.csc.fi/computing/running/example-job-scripts-puhti/)
### Testing 
We will testing if everything will be ok before we submitted to expensive GPU Cluster. 

```bash
sbatch test_rag.sh
tail -f slurm-*
```

### Finetuning

```bash
sbatch run_rag.sh
tail -f slurm-*
```

Wait about 12 hours


