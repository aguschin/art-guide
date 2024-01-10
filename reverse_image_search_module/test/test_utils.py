import os
from PIL import Image
import numpy as np
import logging
from ..utils.vdb_slow import NearestVectorFinder
from ..resnet18 import MULTI_EMBEDDINGS


DATA_IMAGES_PATH = 'data/img/full/'
IMAGE_MAX_NUMBER = 5000

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

embeddings_path = './data/embeddings_multi.npy' if MULTI_EMBEDDINGS else './data/embeddings.npy'
all_embeddings = np.load(embeddings_path)


def test_vector_norm():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    distance = np.linalg.norm(nnvf.vectors, axis=1)

    assert np.alltrue(distance == np.ones_like(distance, dtype=np.float32))


def test_vector_k1():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    distance = np.linalg.norm(nnvf.vectors, axis=1)

    assert np.alltrue(distance == np.ones_like(distance, dtype=np.float32))

    target_vector = np.ones((1,123), dtype=np.float32)
    
    idx, dist = nnvf.get_nns_by_vector(target_vector,
                                       k=1, 
                                       search_k=-1, 
                                       include_distances=True)


    assert idx.dtype == np.int64
    assert dist.dtype == np.float64
    assert len(dist.shape) == 1
    assert len(idx.shape) == 1

    assert idx.shape[0] == 1


def test_vector_k10():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    distance = np.linalg.norm(nnvf.vectors, axis=1)

    assert np.alltrue(distance == np.ones_like(distance, dtype=np.float32))

    target_vector = np.ones((1,123), dtype=np.float32)
    
    idx, dist = nnvf.get_nns_by_vector(target_vector,
                                       k=10, 
                                       search_k=-1, 
                                       include_distances=True)


    assert idx.dtype == np.int64
    assert dist.dtype == np.float64
    assert len(dist.shape) == 1
    assert len(idx.shape) == 1

    assert idx.shape[0] == 10



# def test_utils_nearest_vector_finder():
#     nnvf = NearestVectorFinder(all_embeddings)

#     target_vector = np.ones((all_embeddings.shape[1]), dtype=np.float32)

#     idx, dist = nnvf.get_nns_by_vector(target_vector,
#                            k=1, 
#                            search_k=-1, 
#                            include_distances=True)

    