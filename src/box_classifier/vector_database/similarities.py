import numpy as np
from typing import List
from numpy.typing import NDArray
from src.box_classifier.vector_database.base import BaseSimilarities


class CosineSimilarity(BaseSimilarities[NDArray]):
    def compute(self, query: NDArray, candidates: List[NDArray]) -> List[float]:
        if len(candidates) == 0:
            return []

        matrix = np.vstack(candidates)

        query_norm = np.linalg.norm(query)
        matrix_norm = np.linalg.norm(matrix, axis=1)

        denom = query_norm * matrix_norm
        denom[denom == 0] = 1e-10

        sims = matrix @ query / denom

        return (1 - sims).tolist()
    
class DotProductSimilarity(BaseSimilarities[NDArray]):
    def compute(self, query: NDArray, candidates: List[NDArray]) -> List[float]:
        if len(candidates) == 0:
            return []

        matrix = np.vstack(candidates)
        sims = matrix @ query

        return (-sims).tolist()  # negative so "smallest = best"