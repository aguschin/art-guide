import numpy as np


class NearestVectorFinder:
    def __init__(self, vectors):
        # vectors is a list of vectors you want to compare against
        self.vectors = np.array(vectors, dtype=np.float32) / np.linalg.norm(vectors, axis=1).reshape(-1,1)
        
    def get_nns_by_vector(self, target_vector, k=1, search_k=-1, include_distances=True):
        target_vector = target_vector.squeeze()

        assert len(target_vector.shape) == 1

        # Calculate dot products
        dot_products = np.dot(self.vectors, target_vector)

        # Calculate magnitudes of vectors
        
        target_magnitude = np.linalg.norm(target_vector)

        # Calculate cosine similarities
        cosine_similarities = dot_products / target_magnitude

        # Find the indices of the k nearest vectors
        nearest_indices = np.argsort(cosine_similarities)[-k:][::-1]
        cosine_similarities = cosine_similarities[nearest_indices]

        if include_distances:
            return nearest_indices, cosine_similarities
        else:
            return nearest_indices