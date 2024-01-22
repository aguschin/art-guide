import pickle
import numpy as np
from decouple import config


MULTI_EMBEDDINGS = config('MULTI_EMBEDDINGS') == 'True'

SINGLE_INPUT_FILE = config('SINGLE_INPUT_FILE')
SINGLE_VALES_OUTPUT_FILE = config('SINGLE_VALES_OUTPUT_FILE')
SINGLE_KEYS_OUTPUT_FILE = config('SINGLE_KEYS_OUTPUT_FILE')

MULTI_INPUT_FILE = config('MULTI_INPUT_FILE')
MULTI_VALES_OUTPUT_FILE = config('MULTI_VALES_OUTPUT_FILE')
MULTI_KEYS_OUTPUT_FILE = config('MULTI_KEYS_OUTPUT_FILE')


def extract_embedding(input_file = MULTI_INPUT_FILE, 
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
        extract_embedding(input_file = MULTI_INPUT_FILE, 
                    values_output_file = MULTI_VALES_OUTPUT_FILE,
                    keys_output_file = MULTI_KEYS_OUTPUT_FILE)
    else:
        extract_embedding(input_file = SINGLE_INPUT_FILE,
                     values_output_file = SINGLE_VALES_OUTPUT_FILE,
                     keys_output_file = SINGLE_KEYS_OUTPUT_FILE)