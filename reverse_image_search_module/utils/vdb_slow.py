import numpy as np
from multiprocessing import Pool

def normalize_vector(vector):
    magnitude = np.linalg.norm(vector)
    return vector / magnitude

def parallel_normalize(vectors):
    with Pool() as pool:
        normalized_vectors = pool.map(normalize_vector, vectors)
    return np.array(normalized_vectors, dtype=np.float32)

class NearestVectorFinder:
    def __init__(self, vectors):
        after_squeeeze = len(vectors.shape) - sum([1 if val == 1 else 0 for val in vectors.shape])

        assert after_squeeeze == 2, 'vectors shape most be NxM'
        
        # vectors is a list of vectors you want to compare against
        self.vectors = parallel_normalize(vectors.squeeze())
        
    def get_nns_by_vector(self, target_vector, k=1, search_k=-1, include_distances=True):
        # import ipdb

        # ipdb.set_trace()
        target_vector = target_vector.squeeze()
        target_magnitude = np.linalg.norm(target_vector)
        
        target_vector /= target_magnitude
        
        assert len(target_vector.shape) == 1

        # Calculate dot products
        dot_products = np.dot(self.vectors, target_vector).squeeze()

        dot_products[ np.isnan(dot_products) ] = 0.0

        # Find the indices of the k nearest vectors
        nearest_indices = np.argsort(dot_products)[-k:][::-1]
        dot_products = dot_products[nearest_indices]

        if include_distances:
            return nearest_indices, dot_products
        else:
            return nearest_indices