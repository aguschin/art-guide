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


def test_nearest_vector_finder_norm():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    distance = np.linalg.norm(nnvf.vectors, axis=1)

    assert np.alltrue(np.abs(distance - 1.0) < 1e-6)


def test_nearest_vector_finder_k1():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    target_vector = np.ones((123), dtype=np.float32)
    
    idx, dist = nnvf.get_nns_by_vector(target_vector,
                                       k=1, 
                                       search_k=-1, 
                                       include_distances=True)


    assert idx.dtype == np.int64
    assert len(dist.shape) == 1
    assert len(idx.shape) == 1

    assert idx.shape[0] == 1


def test_nearest_vector_finder_k10():
    vectors = np.ones((5000,123))
    nnvf = NearestVectorFinder(vectors)

    target_vector = np.ones((1,123), dtype=np.float32)
    
    idx, dist = nnvf.get_nns_by_vector(target_vector,
                                       k=10, 
                                       search_k=-1, 
                                       include_distances=True)


    assert idx.dtype == np.int64
    assert len(dist.shape) == 1
    assert len(idx.shape) == 1

    assert idx.shape[0] == 10


def test_utils_nearest_vector_finder():
    all_embeddings = np.load(embeddings_path)

    nnvf = NearestVectorFinder(all_embeddings)

    L = all_embeddings.shape[0] - 1

    for i in [0, L, L//2]:
        target_vector = all_embeddings[i]

        idx, _ = nnvf.get_nns_by_vector(target_vector,
                            k=1, 
                            search_k=-1, 
                            include_distances=True)
        
        assert idx[0] == i