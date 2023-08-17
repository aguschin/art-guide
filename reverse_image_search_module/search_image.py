from annoy import AnnoyIndex
from matplotlib import pyplot as plt

from reverse_image_search_module.resnet18 import img2vec
import numpy as np
import pandas as pd

# Load all embeddings from the .npy file
all_embeddings = np.load('./data/all_embeddings.npy')
embedding_dim = all_embeddings.shape[1]

# Build Annoy index
annoy_index = AnnoyIndex(embedding_dim, metric='dot')  # using dot, while assuming the vectors are normalized

for idx, vec in enumerate(all_embeddings):
    vec = vec / np.linalg.norm(vec)
    annoy_index.add_item(idx, vec)

num_trees = 50
annoy_index.build(num_trees)

dataset = pd.read_csv('./data/wikiart_scraped.csv')


def change_format(data):
    return {
        'author_name': data['Artist'],
        'art_name': data['Artwork'],
        'style': data['Style'],
        'date': data['Date']
    }


def find_image(img):
    plt.imshow(img)
    plt.show()

    vector = img2vec.getNormalizedVec(img)
    idx, dist = annoy_index.get_nns_by_vector(vector, 1, search_k=-1, include_distances=True)
    idx, dist = idx[0], dist[0]
    data = change_format(dataset.iloc[idx].to_dict())

    return idx, dist, data
