import pickle
import numpy as np
input_file = '/root/art-guide/image_search_modified/embeddings_full.pkl'
# input_file = "/Users/mohammadsanaee/Documents/harbour/art projrct/art-guide/data/embeddings_full.pkl"
values_output_file = '/root/art-guide/image_search_modified/embeddings.npy'
keys_output_file = '/root/art-guide/image_search_modified/file_names.npy'
# keys_output_file = '/Users/mohammadsanaee/Documents/harbour/art projrct/art-guide/data/embeddings_test.npy'
# values_output_file = '/Users/mohammadsanaee/Documents/harbour/art projrct/art-guide/data/file_names_test.npy'

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