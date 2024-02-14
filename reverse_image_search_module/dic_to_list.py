import pickle
import numpy as np
from decouple import config


MULTI_EMBEDDINGS = bool(config('MULTI_EMBEDDINGS'))

SINGLE_INPUT_FILE = config('SINGLE_INPUT_FILE')
SINGLE_VALES_OUTPUT_FILE = config('SINGLE_VALES_OUTPUT_FILE')
SINGLE_KEYS_OUTPUT_FILE = config('SINGLE_KEYS_OUTPUT_FILE')

MULTI_INPUT_FILE = config('MULTI_INPUT_FILE')
MULTI_VALES_OUTPUT_FILE = config('MULTI_VALES_OUTPUT_FILE')
MULTI_KEYS_OUTPUT_FILE = config('MULTI_KEYS_OUTPUT_FILE')


def single_embedding(input_file = SINGLE_INPUT_FILE,
                     values_output_file = SINGLE_VALES_OUTPUT_FILE,
                     keys_output_file = SINGLE_KEYS_OUTPUT_FILE):

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


def multi_embedding(input_file = MULTI_INPUT_FILE, 
                    values_output_file = MULTI_VALES_OUTPUT_FILE,
                    keys_output_file = MULTI_KEYS_OUTPUT_FILE):
    
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
    if MULTI_EMBEDDINGS:
        multi_embedding()
    else:
        single_embedding()
