import numpy as np
import re
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import pdist, squareform
from tqdm import tqdm


def normalize_data(data, method='z-score'):
    """
    Normalize the data.

    Parameters:
    data (numpy.ndarray): The data to normalize.
    method (str, optional): The normalization method ('min-max' or 'z-score').

    Returns:
    numpy.ndarray: Normalized data.
    """
    if method == 'min-max':
        min_val = np.min(data)
        max_val = np.max(data)
        normalized = (data - min_val) / (max_val - min_val)
    elif method == 'z-score':
        mean = np.mean(data)
        std = np.std(data)
        normalized = (data - mean) / std
    else:
        raise ValueError("Unknown normalization method.")

    return normalized

def compute_signal_similarity(data_sets, signal_index):
    """
    Compute the similarity matrix for a specific type of signal.

    Parameters:
    data_sets (list of tuples or lists): A list of data sets, where each data set contains multiple signals.
    signal_index (int): The index of the signal to compute similarity for.

    Returns:
    numpy.ndarray: A similarity matrix for the specified signal.
    """

    # Extract the specific signal from each data set
    # specific_signals = [data_set[signal_index] for data_set in data_sets]
    expected_length = 7
    pad_value = 0
    # Extract and pad the specific signal from each data set
    specific_signals = []
    for data_set in tqdm(data_sets):
        signal = data_set[signal_index]
        if (expected_length - len(signal)) != 0:
            print(expected_length - len(signal))
        padded_signal = list(signal) + [pad_value] * (expected_length - len(signal))
        specific_signals.append(padded_signal[:expected_length])
        
    # Normalize the signals
    flattened_signals = np.array(specific_signals)
    # for i in range(flattened_signals.shape[1]):
    #     flattened_signals[:, i] = normalize_data(flattened_signals[:, i], "min-max")

    # Flatten each signal and compute pairwise Euclidean distance
    
    distances = pdist(flattened_signals, 'euclidean')
    distance_matrix = squareform(distances)

    # Convert distances to similarities
    similarity_matrix = 1 / (1 + distance_matrix)
    
    print(np.mean(similarity_matrix))
    
    return similarity_matrix

def aggregate_similarities(data_sets, num_signals):
    """
    Aggregate the similarities of each signal type into a combined similarity measure.

    Parameters:
    data_sets (list of tuples or lists): A list of data sets, where each data set contains multiple signals.
    num_signals (int): The number of different signals in each data set.

    Returns:
    numpy.ndarray: A combined similarity matrix.
    """
    combined_similarity = np.zeros((len(data_sets), len(data_sets)))
    weight = [0.70702137, 0.0485446,  0.17451003, 0.069924]
    # manual = []
    # weight = [w[j]*manual[j] for j in range(4)]
    # weight = [(j/sum(weight)) for j in weight]
    print(weight)
    # normv = [0.25,0.25,0.25,0.25] # S Cur Acc Cour
    name = ['speed','curvature','acceleration','course']
    for i in [0,1,2,3]:
        signal_similarity = compute_signal_similarity(data_sets, i)
        # np.save(f'{name[i]}.npy', signal_similarity)
        combined_similarity += weight[i] * signal_similarity

    # Average the combined similarities
    # combined_similarity /= num_signals

    return combined_similarity


def extract_vehicle_signals(input_string):
    # Patterns for matching speed, curvature, acceleration, and course data
    speed_pattern = r"Speed: \[([0-9., -]+)\]"
    curvature_pattern = r"Curvature: \[([0-9., -]+)\]"
    acceleration_pattern = r"Acceleration: \[([0-9., -]+)\]"
    course_pattern = r"Course: \[([0-9., -]+)\]"

    # Function to extract and convert data to a list of floats
    def extract_data(pattern):
        match = re.search(pattern, input_string)
        return [float(x) for x in match.group(1).split(',')] if match else []

    # Extract data
    speed = extract_data(speed_pattern)
    curvature = extract_data(curvature_pattern)
    acceleration = extract_data(acceleration_pattern)
    course = extract_data(course_pattern)

    return speed, curvature, acceleration, course



def get_normal_embedding(dataset, strategy):

    if dataset == "BDDX":
        train_conv_path = "./video_process/final_conv_base/conversation_bddx_train.json"
        test_conv_path = "./video_process/final_conv_base/conversation_bddx_eval.json"
            
        with open(train_conv_path,"r") as ftr:
            train_conv = json.load(ftr)
        with open(test_conv_path,"r") as fte:
            test_conv = json.load(fte)
        conv = train_conv + test_conv
        # Load embeddings
        vp_emb_match = {}

        npz_file = np.load("./retrieval/embeddings_project.npz")
        for key in npz_file:
            vp_emb_match[key] = npz_file[key]
        npz_file.close()
        vp_conversation_match = {ele["video"]: ' '.join([ele["conversations"][1]['value'],ele["conversations"][3]['value']]) for ele in conv}
        # Info Match
        with open("./retrieval/bddx_vpath_info_match.json",'r') as im:
            vp_info = json.load(im)

        vp_signal_match = {vp['video']: vp_info[vp['video']] for vp in conv}
        
        
    elif dataset == 'SAX':
        train_conv_path = "./video_process/final_conv_base/conversation_bddx_train.json"
        test_conv_path = "./video_process/final_sax_conv_base/conversation_sax_eval.json"
        with open(train_conv_path,"r") as ftr:
            train_conv = json.load(ftr)
        with open(test_conv_path,"r") as fte:
            test_conv = json.load(fte)
        conv = train_conv + test_conv
                # Load embeddings
        vp_emb_match = {}
        npz_file1 = np.load("./video_process/SAX/new_emb/embeddings.npz")
        npz_file2 = np.load("./video_process/BDDX_Processed/new_emb/embeddings.npz")
        for key in npz_file1:
            vp_emb_match[key] = npz_file1[key]
        npz_file1.close()
        for key in npz_file2:
            vp_emb_match[key] = npz_file2[key]
        npz_file2.close()
        vp_conversation_match = {ele["video"][0]: ' '.join([ele["conversations"][1]['value'],ele["conversations"][3]['value']]) for ele in conv}
        vp_signal_match = None
    vpath_lis = [vp for vp in vp_emb_match]
    sorted_video_ids = [i for i in range(len(vpath_lis))]
    vpath_id_match = {i:vpath_lis[i] for i in range(len(vpath_lis))}
    
    # Process embeddings
    
    
    embeddings = np.array([vp_emb_match[vp] for vp in vp_emb_match])
    embeddings = embeddings.reshape(embeddings.shape[0], embeddings.shape[2])
    print("EMB SHAPE",embeddings.shape)

    norm_embeddings = embeddings
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    return norm_embeddings, vp_conversation_match, sorted_video_ids, vpath_id_match, vp_signal_match

def get_similarity(norm_embeddings):
    
    similarities = cosine_similarity(norm_embeddings)
        
    return similarities


if __name__ == "__main__":
    k = 2
    dataset = 'SAX'
    
    retr_strategy = "hybrid"
    
    norm_embeddings, vp_conversation_match, sorted_video_ids, vpath_id_match, vp_signal_match = get_normal_embedding(dataset, retr_strategy)

    combined_similarity = get_similarity(norm_embeddings)

    # Determine top k similar videos (assuming k is defined)
    top_k_indices = np.argsort(-combined_similarity, axis=1)[:, 1:100]

    # Update the Similarity Dictionary with combined similarities
    cosine_similarity_dict = {sorted_video_ids[i]: [sorted_video_ids[j] for j in top_k_indices[i]] for i in range(len(sorted_video_ids))}
    
    # ID Match to vpath match
    final_vpath_match = {}
    for key, val in cosine_similarity_dict.items():
        cur_k = vpath_id_match[key]
        cur_v = [vpath_id_match[v] for v in val]
        final_vpath_match.update({cur_k:cur_v})
        
    # Filter Test In Train
    t_dict = {}
    for key, val in final_vpath_match.items():
        v = [vp for vp in val]
        v = v[:k]
        t_dict.update({key:v})
        
    final_vpath_match = t_dict
    

    # Save the cosine similarity dictionary
    if dataset == 'BDDX':
        with open(f"./retrieval/BDDX_RAG_{retr_strategy}_vpmatch_t13.json", "w") as f:
            json.dump(final_vpath_match, f, indent=4)
            
    elif dataset == 'SAX':
        with open(f"./retrieval/SAX_RAG_{retr_strategy}_vpmatch.json", "w") as f:
            json.dump(final_vpath_match, f, indent=4)