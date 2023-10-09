import torch
from annoy import AnnoyIndex
import ast
from .resnet18 import img2vec
import numpy as np
import pandas as pd

# Load all embeddings from the .npy filessssssssssssssssssss
all_embeddings = np.load('./data/embeddings.npy')
embedding_dim = all_embeddings.shape[2]
file_names = np.load('./data/file_names.npy')

# Build Annoy index
annoy_index = AnnoyIndex(embedding_dim, metric='dot')  # using dot, while assuming the vectors are normalized

for idx, vec in enumerate(all_embeddings):
    vec = vec.squeeze()
    vec = vec / np.linalg.norm(vec)
    annoy_index.add_item(idx, vec)

num_trees = 50
annoy_index.build(num_trees)

dataset = pd.read_csv('./data/data.csv',low_memory=False)
dataset['images'].fillna('[]', inplace=True)

dataset['images'] = dataset['images'].apply(ast.literal_eval)

def extract_file_name(x):
    if isinstance(x, list) and len(x) > 0:
        return x[0]['path'].split('/')[-1]
    else:
        return None

dataset['file_name'] = dataset['images'].apply(extract_file_name)

def change_format(data):
    return {
        'author_name': data['Author'],
        'style': data['Styles'],
        'date': data['Date'],
        'id': data['Id'],
        'url': data['URL'],
        'title': data['Title'],
        'original_title': data['OriginalTitle'],
        'series': data['Series'],
        'genre': data['Genre'],
        'media': data['Media'],
        'location': data['Location'],
        'dimension': data['Dimensions'],
        'description': data['WikiDescription'],
        'tags': data['Tags'],
        'image_url': data['image_urls'],
    }


def find_image(img):

    vector = img2vec.getVectors(img)
    vector = np.transpose(vector)
    vector = vector / np.linalg.norm(vector)

    idx, dist = annoy_index.get_nns_by_vector(vector, 1, search_k=-1, include_distances=True)
    idx, dist = idx[0], dist[0]
    file_n = file_names[idx]
    matching_idx = dataset[dataset['file_name'] == file_n].index
    data = change_format(dataset.loc[matching_idx].to_dict())
    return idx, dist, data
