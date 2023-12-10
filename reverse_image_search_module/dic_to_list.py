import pickle
import numpy as np


def single_embedding():
    input_file = '../data/embeddings_full.pkl'
    values_output_file = '../data/embeddings.npy'
    keys_output_file = '../data/file_names.npy'

    with open(input_file, 'rb') as f:
        data_dict = pickle.load(f)

    keys = list(data_dict.keys())
    values = list(data_dict.values())
    # Check if all values have the same shape
    value_shapes = set(val.shape for val in values)
    if len(value_shapes) != 1:
        raise ValueError("All values in the dictionary must have the same shape.")
    keys_array = np.array(keys)
    values_array = np.array(values)
    np.save(keys_output_file, keys_array)
    np.save(values_output_file, values_array)


def multi_embedding():
    input_file = 'image_search_modified/embeddings_full.pkl'
    values_output_file = 'data/embeddings.npy'
    keys_output_file = 'data/file_names.npy'
    
    with open(input_file, 'rb') as f:
        data_dict = pickle.load(f)
    
    keys = []
    values = []

    for k, v in data_dict.items():
        keys += [k] * len(v)
        values += v
    
    keys = np.array(keys)
    values = np.array(values)

    np.save(keys_output_file, keys)
    np.save(values_output_file, values)


if __name__ == '__main__':
    single_embedding()