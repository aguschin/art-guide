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

dataset = pd.read_csv('./data/data.csv')


def change_format(data):
    return {
        'author_name': data['Author'],
        # 'art_name': data['Artwork'],
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
        'dimention': data['Dimentions'],
        'description': data['WikiDescription'],
        'tags': data['Tags'],
        'image': data['img'],
        'image_url': data['image_urls']

    }


def find_image(img):
    print("Image\n", img)
    plt.imshow(img)
    plt.show()

    # img = img2vec.preprocess_image(img)
    vec = img2vec.getVectors(img)
    # vector = img2vec.getNormalizedVec(img)
    vector = vec / np.linalg.norm(vec)

    idx, dist = annoy_index.get_nns_by_vector(vector, 1, search_k=-1, include_distances=True)
    idx, dist = idx[0], dist[0]
    data = change_format(dataset.iloc[idx].to_dict())

    return idx, dist, data
