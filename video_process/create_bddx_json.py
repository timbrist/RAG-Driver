import os
import json
import numpy as np
from tqdm import tqdm 
import random
import math


def uniform_sample(lst, num_samples):
    sample = lst[::4]
    # sample = [round(float(s),2) for s in sample]
    sample = [round(s,2) for s in sample]
    return sample

def random_subset(sample_list):
    """
    Randomly selects a varying number of elements (1 to 5) from the provided list.

    Parameters:
    sample_list (list): The list from which to select elements.

    Returns:
    list: A list containing a random subset of the original list.
    """
    # Randomly choose how many elements to select (between 1 and 5)
    # num_elements = random.randint(1, min(5, len(sample_list)))
    num_elements = 2
    # Randomly select the elements
    return random.sample(sample_list, num_elements)

def get_car_info(car_info, predict_cs=False):
    speed = uniform_sample(car_info['speed'],8)
    curvature = uniform_sample(car_info['curvature'],8)
    # print(curvature)
    acceleration = uniform_sample(car_info['acceleration'],8)
    course = uniform_sample(car_info['course'],8)
    
    # Context
    if predict_cs:
        final_cs = f'Speed: {speed[-1]} Course: {course[-1]}'
        speed, curvature, acceleration, course = speed[:-1], curvature[:-1], acceleration[:-1], course[:-1]    
        # final_cs = [speed[-1], curvature[-1], acceleration[-1], course[-1]]
    else:
        final_cs = None
        
    context = f"The current video records driving scenario: <video>\n Control Signal until current Frame Sequence is: Speed: {speed}\n Curvature: {curvature}\n Acceleration: {acceleration}\n Course: {course}"
    return context, final_cs


import os
WORKSPACE = os.getcwd()

def main(split):
    if split == "train":
        info_root = f"{WORKSPACE}/video_process/BDDX_Processed/info"
    elif split == "test":
        info_root = f"{WORKSPACE}/video_process/BDDX_Test/info"
        
    question_1 = '''What is the action of ego car?'''
    question_2 = '''Why does the ego car doing this?'''
    question_3 = '''Predict the control signal for next frame.'''
    control_signal = True
    # RAG ICL
    rag = False
    strategy = 'hybird'
    # strategy = 'visual'

    # match_path = f"../retrieval/BDDX_RAG_{strategy}_vpmatch_t9.json"
    match_path = f"{WORKSPACE}/retrieval/BDDX_RAG_tuned_vpmatch_t13.json"
    id_info_path = f"{WORKSPACE}/retrieval/bddx_vpath_info_match.json"

    if rag:
        with open(match_path,"r") as fm:
            match_dict = json.load(fm)
        with open(id_info_path,"r") as fi:
            id_info_match = json.load(fi)
    # Add eval
    add_eval = False
    if add_eval and split == "train":
        info_root = "./BDDX_ALL/info"
        
    predict_cs = True
    
    new_info_lis = []
    for root, dirs, files in os.walk(info_root):
        for f in tqdm(files):
            info_path = os.path.join(root,f)
            with open(info_path,"r") as inf:
                info = json.load(inf)
                idx, video_path, conversation, car_info = info['id'], info['video'], info['comment'], info['car_info']
                # print(conversation)
                action, justification = conversation[0]['action'], conversation[1]['justification']
                # print(car_info)
                vk = video_path.split("/",5)[-1]
                if control_signal and rag:
                    # RAG 

                    matched_ids = match_dict[vk]
                    matched_samples = [id_info_match[sid] for sid in matched_ids]
                    if len(matched_samples) != 2:
                        raise NameError
                        
                    # matched_samples = random_subset(matched_samples)
                    icl_context = "Here are also some historical driving experience and corresponding question answering for your reference:"
                    for icl_id, sample in enumerate(matched_samples):
                        # sample = sample.replace("<video>","")
                        icl_context += f"Experience {icl_id}:{sample}\n"
                    icl_context += "*" * 60
                    
                    # else:
                    #     icl_context = "Here are also some historical driving experience for your reference: No Past Experience"
                    #     icl_context += "*" * 60

                    # Context
                    context,final_cs = get_car_info(car_info,predict_cs)
                    
                    if predict_cs:
                        new_conversation = [    
                            # {'from':'human','value':f'{context}\n{icl_context}\n{question_1}'},
                            {'from':'human','value':f'{icl_context}\n{context}\n{question_1}'},
                            {'from':'gpt','value':f'{action}'},
                            {'from':'human','value':f'{question_2}'},
                            {'from':'gpt','value':f'{justification}'},
                            {'from':'human','value':f'{question_3}'},
                            {'from':'gpt','value':f'{final_cs}'},
                        ]                        
                    else:
                        new_conversation = [    
                            # {'from':'human','value':f'{context}\n{icl_context}\n{question_1}'},
                            {'from':'human','value':f'{icl_context}\n{context}\n{question_1}'},
                            {'from':'gpt','value':f'{action}'},
                            {'from':'human','value':f'{question_2}'},
                            {'from':'gpt','value':f'{justification}'}
                        ]
                    
                    
                elif control_signal and not rag:
                    
                    context,final_cs = get_car_info(car_info,predict_cs)
                    if predict_cs:
                        new_conversation = [    
                            {'from':'human','value':f'{context}\n{question_1}'},
                            {'from':'gpt','value':f'{action}'},
                            {'from':'human','value':f'{question_2}'},
                            {'from':'gpt','value':f'{justification}'},
                            {'from':'human','value':f'{question_3}'},
                            {'from':'gpt','value':f'{final_cs}'}
                        ]      
                    else:
                        new_conversation = [    
                            {'from':'human','value':f'{context}\n{question_1}'},
                            {'from':'gpt','value':f'{action}'},
                            {'from':'human','value':f'{question_2}'},
                            {'from':'gpt','value':f'{justification}'}
                        ]                         
                
                else:
                    new_conversation = [
                        {'from':'human','value':f'{question_1}'},
                        {'from':'gpt','value':f'{action}'},
                        {'from':'human','value':f'{question_2}'},
                        {'from':'gpt','value':f'{justification}'}
                    ]
                video_path = video_path.split("/",1)[-1]
                if rag:
                    rag_path = match_dict[video_path]
                    all_video_path = rag_path + [video_path]
                else:
                    all_video_path = [video_path]
                
                info_dict = {
                    "id": f"{idx}",
                    "video": all_video_path,
                    "conversations": new_conversation
                }
                new_info_lis.append(info_dict)
                # break

    
    
    
    sp = "train" if split == "train" else "eval"
    out_dir = f"{WORKSPACE}/video_process/conv_base"
    os.makedirs(out_dir,exist_ok=True)
    out_path = f'{out_dir}/conversation_bddx_{sp}.json'
    
    # if split == 'train':
    #     with open (f'{out_dir}/conversation_bddx_eval.json','r') as ft:
    #         de = json.load(ft)
    #     des = random.sample(de, 256)
    #     new_info_lis += des
    
    
    with open(out_path, 'w') as f:
        json.dump(new_info_lis, f)
        

if __name__ == "__main__":
    main("test")
    main("train")
    