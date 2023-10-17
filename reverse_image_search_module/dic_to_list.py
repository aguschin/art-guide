import pickle
import numpy as np
input_file = '../data/embeddings_full.pkl'
values_output_file = '../data/embeddings.npy'
keys_output_file = '../data/file_names.npy'


with open(input_file, 'rb') as f:
    data_dict = pickle.load(f)

keys = list(data_dict.keys())
values = list(data_dict.values())
import ipdb
#ipdb.set_trace()
# Check if all values have the same shape
value_shapes = set()
for index,val in enumerate(values):
    try:
        shape = val.shape
    except AttributeError:
       values[index]=np.zeros((1,768))
	 #print(f"Value without shape at index {index}: {val}")
       continue
    value_shapes.add(shape)

#value_shapes = set(val.shape for val in values)
#if len(value_shapes) != 1:
# `   raise ValueError("All values in the dictionary must have the same shape.")
print(value_shapes)
keys_array = np.array(keys)
values_array = np.array(values)
np.save(keys_output_file, keys_array)
np.save(values_output_file, values_array)
