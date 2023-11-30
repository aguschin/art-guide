from annoy import AnnoyIndex
import ast
from .resnet18 import img2vec
import numpy as np
import pandas as pd
import torchvision.transforms as transforms
from PIL import Image

# Load all embeddings from the .npy filessssssssssssssssssss
all_embeddings = np.load('./data/embeddings.npy')
embedding_dim = all_embeddings.shape[2]
file_names = np.load('./data/file_names.npy')

# Build Annoy index
# using dot, while assuming the vectors are normalized
annoy_index = AnnoyIndex(embedding_dim, metric='dot')

for idx, vec in enumerate(all_embeddings):
    vec = vec.squeeze()
    vec = vec / np.linalg.norm(vec)
    annoy_index.add_item(idx, vec)

num_trees = 50
annoy_index.build(num_trees)

dataset = pd.read_csv('./data/data.csv',
                      low_memory=False)
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


def find_index_from_image(img, n):
    if isinstance(img, np.ndarray):
        img = Image.fromarray((img * 255).astype(np.uint8))
    tra = transforms.Compose([transforms.Resize((224, 224))])
    img = tra(img)
    vector = img2vec.getVectors(img)
    vector = np.transpose(vector)

    norm = np.linalg.norm(vector)

    # in case it is 0
    vector = vector / (norm + 1e-9)

    idx, dist = annoy_index.get_nns_by_vector(vector,
                                              n,
                                              search_k=-1,
                                              include_distances=True)

    return idx, dist


def find_file_name(idx):
    return file_names[idx]


def find_image(img, n=1):
    idx, dist = find_index_from_image(img, n)

    file_n = find_file_name(idx[0])

    matching_idx = dataset[dataset['file_name'] == file_n].index.values[0]
    data = change_format(dataset.loc[matching_idx].to_dict())
    if n == 1:
        return idx[0], dist[0], data
    return idx, dist, data
