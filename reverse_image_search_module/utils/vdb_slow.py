import numpy as np


class NearestVectorFinder:
    def __init__(self, vectors):
        # vectors is a list of vectors you want to compare against
        self.vectors = np.array(vectors)
        self.vector_magnitudes = np.linalg.norm(self.vectors, axis=1)

    def get_nns_by_vector(self, target_vector, k=1, search_k=-1, include_distances=True):
        # Calculate dot products
        dot_products = np.dot(self.vectors, target_vector)

        # Calculate magnitudes of vectors
        
        target_magnitude = np.linalg.norm(target_vector)

        # Calculate cosine similarities
        cosine_similarities = dot_products / (self.vector_magnitudes * target_magnitude)

        # Find the indices of the k nearest vectors
        nearest_indices = np.argsort(cosine_similarities)[-k:][::-1]

        # Return the k nearest vectors and their cosine similarities
        nearest_vectors = self.vectors[nearest_indices]
        cosine_similarities = cosine_similarities[nearest_indices]

        if include_distances:
            return nearest_vectors, cosine_similarities
        else:
            return nearest_vectors