from pathlib import Path
from typing import List, Tuple, Dict
import json
import numpy as np
from numpy.typing import NDArray

from src.box_classifier.domains import BoxType
from src.box_classifier.vector_database.base import BaseSimilarities, BaseNumpyVectordatabase


class JsonVectorDatabase(BaseNumpyVectordatabase):
    def __init__(self, similarity: BaseSimilarities[NDArray]) -> None:
        self._data: Dict[BoxType, NDArray] = {}
        self._similarity = similarity

    def add(self, id: BoxType, vector: NDArray) -> None:
        self._data[id] = vector

    def get(self, id: BoxType) -> NDArray:
        return self._data[id]

    def get_many(self, ids: List[BoxType]) -> List[NDArray]:
        return [self._data[i] for i in ids]

    def get_smallest(self, query: NDArray, top_k: int = 1) -> List[Tuple[BoxType, float]]:
        ids = list(self._data.keys())
        vectors = list(self._data.values())

        scores = self._similarity.compute(query, vectors)
        pairs = list(zip(ids, scores))

        pairs.sort(key=lambda x: x[1])
        return pairs[:top_k]

    def delete(self, ids: List[BoxType]) -> None:
        for i in ids:
            self._data.pop(i, None)

    def save(self, path: Path) -> None:
        serializable_data = {
            str(k): v.tolist() for k, v in self._data.items()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f)

    def load(self, path: Path) -> None:
        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as f:
            raw: Dict[str, List[float]] = json.load(f)

        self._data = {
            BoxType(k): np.array(v) for k, v in raw.items()
        }