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


## Data Preparation

Processed Version of BDD-X is available from [here](https://drive.google.com/file/d/14a3QTkWRelAZs-kW_2U5tjYcAm2l8VbF/view)

**Please unzip the file into video_process folder**

First, we need to create the conversation dataset. 
And second, we move the data to project workspace, because the file: BDDX_RAG_hybird_vpmatch.json using the relative path.
Later, I want to update every path to absolute path. 

```bash
cd video_process
python create_bddx_json.py
cd ..
mv video_process/BDD_Processed ./BDD_Processed
mv video_process/BDD_Test ./BDD_Test
```


## Finetuning

```bash
sbatch run_rag.sh
tail -f slurm-*
```

Wait about 12 hours


