# This script only for those who can't not use git lfs on cluster 

# export WORKSPACE=/projappl/project_2010633/RAG-Driver
export WORKSPACE=$(pwd)


export VIDEO_LLAVA=${WORKSPACE}/models/Video-LLaVA-7B
export VIDEO_LLAVA_PRETRAIN=${WORKSPACE}/models/Video-LLaVA-Pretrain-7B
export LANGUAGEBIN_VIDEO=${WORKSPACE}/models/LanguageBind_Video_merge
export LANGUAGEBIN_IMAGE=${WORKSPACE}/models/LanguageBind_Image


#Download the checkpoint from hugginface without large file
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/LanguageBind/Video-LLaVA-7B ${VIDEO_LLAVA}
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/LanguageBind/Video-LLaVA-Pretrain-7B ${VIDEO_LLAVA_PRETRAIN}
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/LanguageBind/LanguageBind_Video_merge ${LANGUAGEBIN_VIDEO}
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/LanguageBind/LanguageBind_Image ${LANGUAGEBIN_IMAGE}

# download video llava large file using wget manually
wget https://huggingface.co/LanguageBind/Video-LLaVA-7B/resolve/main/tokenizer.model?download=true \
    O ${VIDEO_LLAVA}/tokenizer.model

wget https://huggingface.co/LanguageBind/Video-LLaVA-7B/resolve/main/model-00001-of-00002.safetensors?download=true \
    -O ${VIDEO_LLAVA}/model-00001-of-00002.safetensors \

wget https://huggingface.co/LanguageBind/Video-LLaVA-7B/resolve/main/model-00002-of-00002.safetensors?download=true \
    -O ${VIDEO_LLAVA}/model-00002-of-00002.safetensors \

wget https://huggingface.co/LanguageBind/Video-LLaVA-7B/resolve/main/pytorch_model-00001-of-00002.bin?download=true \
    -O ${VIDEO_LLAVA}/pytorch_model-00001-of-00002.bin \

wget https://huggingface.co/LanguageBind/Video-LLaVA-7B/resolve/main/pytorch_model-00002-of-00002.bin?download=true \
    -O ${VIDEO_LLAVA}/pytorch_model-00002-of-00002.bin \

wget https://huggingface.co/LanguageBind/Video-LLaVA-Pretrain-7B/resolve/main/mm_projector.bin?download=true \
    -O ${VIDEO_LLAVA_PRETRAIN}/Video-LLaVA-Pretrain-7B/mm_projector.bin \

wget https://huggingface.co/LanguageBind/LanguageBind_Video_merge/resolve/main/pytorch_model.bin?download=true \
    -O ${LANGUAGEBIN_VIDEO}/LanguageBind_Video_merge/pytorch_model.bin \

wget https://huggingface.co/LanguageBind/LanguageBind_Image/resolve/main/pytorch_model.bin?download=true \
    -O ${LANGUAGEBIN_IMAGE}/LanguageBind_Image/pytorch_model.bin

