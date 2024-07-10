# !/bin/
#####################
DATA_ROOT="video_process"
export WORKSPACE=/home/yan/projects/RAG-Driver
export DATA_ROOT=${WORKSPACE}/video_process
export MODELS_ROOT=${WORKSPACE}/models

HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=0 CUDA_VISIBLE_DEVICES=0 deepspeed ${WORKSPACE}/llava/train/train_mem.py \
    --deepspeed ${WORKSPACE}/scripts/zero3_offload.json \
    --output_dir ${MODELS_ROOT}/Video-LLaVA-7B_RAGDRIVER \
    --model_name_or_path ${MODELS_ROOT}/checkpoints/Video-LLaVA-7B \
    --version v1 \
    --train_data_path video_process/final/conversation_bddx_train.json \
    --eval_data_path video_process/final/conversation_bddx_eval.json \
    --video_folder ${DATA_ROOT} \
    --image_folder ${DATA_ROOT} \
    --X "Video" "Image" \
    --video_tower ${MODELS_ROOT}/LanguageBind_Video_merge \
    --image_tower ${MODELS_ROOT}/LanguageBind_Image \
    --pretrain_mm_mlp_adapter ${MODELS_ROOT}/Video-LLaVA-Pretrain-7B/mm_projector.bin \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_x_start_end False \
    --mm_use_x_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length False \
    --bf16 True \
    --num_train_epochs 2 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 130 \
    --save_total_limit 5 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to tensorboard \
    --cache_dir "${WORKSPACE}/cache_dir"

echo "Finished 1"

