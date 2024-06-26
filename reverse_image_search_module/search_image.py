import ast
import time

import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from PIL import Image
from torchvision import transforms

from .resnet18 import (
    MULTI_EMBEDDINGS,
    MULTI_KEYS_OUTPUT_FILE,
    MULTI_VALES_OUTPUT_FILE,
    SINGLE_KEYS_OUTPUT_FILE,
    SINGLE_VALES_OUTPUT_FILE,
    gen_multi_cropping,
    img2vec,
)
from .utils.vdb_slow import NearestVectorFinder

dataset = None
annoy_index = None
file_names = None


def extract_file_name(x):
    if isinstance(x, list) and len(x) > 0:
        return x[0]["path"].split("/")[-1]
    else:
        return None


def load_vector_db(multi=MULTI_EMBEDDINGS, reload=False, vdb=True):
    global dataset
    global annoy_index
    global file_names

    if (
        dataset is not None
        and annoy_index is not None
        and file_names is not None
        and not reload
    ):
        return

    embeddings_path = MULTI_VALES_OUTPUT_FILE if multi else SINGLE_VALES_OUTPUT_FILE
    embeddings_filename_path = (
        MULTI_KEYS_OUTPUT_FILE if multi else SINGLE_KEYS_OUTPUT_FILE
    )

    all_embeddings = np.load(embeddings_path)
    embedding_dim = all_embeddings.shape[1]
    file_names = np.load(embeddings_filename_path)

    if vdb:
        print("Loaded annoy")
        # Build Annoy index
        # using dot, while assuming the vectors are normalized
        annoy_index = AnnoyIndex(embedding_dim, metric="dot")

        for idx, vec in enumerate(all_embeddings):
            vec = vec.squeeze()
            vec = vec / np.linalg.norm(vec)
            annoy_index.add_item(idx, vec)

        num_trees = 50
        annoy_index.build(num_trees)
        print(f"names size: {file_names.shape}")
        print(f"embedding size: {all_embeddings.shape}")

    else:
        print("Loaded slow db:", embeddings_path, embeddings_filename_path)

        annoy_index = NearestVectorFinder(all_embeddings)
    dataset = pd.read_csv("./data/data.csv", low_memory=False)
    dataset["images"].fillna("[]", inplace=True)

    dataset["images"] = dataset["images"].apply(ast.literal_eval)

    dataset["file_name"] = dataset["images"].apply(extract_file_name)


load_vector_db()


def change_format(data):
    return {
        "author_name": data["Author"],
        "style": data["Styles"],
        "date": data["Date"],
        "id": data["Id"],
        "url": data["URL"],
        "title": data["Title"],
        "original_title": data["OriginalTitle"],
        "series": data["Series"],
        "genre": data["Genre"],
        "media": data["Media"],
        "location": data["Location"],
        "dimension": data["Dimensions"],
        "description": data["WikiDescription"],
        "tags": data["Tags"],
        "image_url": data["image_urls"],
        "file_name": data["file_name"],
    }


def find_file_name(idx):
    return file_names[idx]


def find_index_from_image(img, n, times_to_crop=5):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    idxs, dists = [], []

    for x, y, x_end, y_end in gen_multi_cropping(
        img.width, img.height, k=times_to_crop
    ):
        # import ipdb; ipdb.set_trace() # 36301 Guernica
        croped = img.crop((x, y, x_end, y_end))

        vector = img2vec.getVectors(croped)
        vector = np.transpose(vector)
        norm = np.linalg.norm(vector)
        vector = vector / norm

        idx, dist = annoy_index.get_nns_by_vector(
            vector, n, search_k=-1, include_distances=True
        )
        idxs.extend(idx)
        dists.extend(dist)

    # sort and get top n
    sorted_indices = sorted(range(len(dists)), key=lambda i: dists[i], reverse=True)
    idxs = [idxs[i] for i in sorted_indices][:n]
    dists = [dists[i] for i in sorted_indices][:n]

    return idxs, dists


def find_image(img, n=1):
    if type(n) != int:
        n = 1

    idx, dist = find_index_from_image(img, n)
    file_n = find_file_name(idx)

    selected_indices = dataset[dataset["file_name"].isin(file_n)].index.tolist()

    selected_data = dataset.loc[selected_indices]

    data = selected_data.apply(
        lambda row: change_format(row.to_dict()), axis=1
    ).tolist()
    return idx, dist, data
