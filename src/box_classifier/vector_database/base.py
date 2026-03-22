from pathlib import Path
from typing import List, Tuple, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from src.box_classifier.domains import BoxType
    from numpy.typing import NDArray
    from torch import Tensor

T = TypeVar("T")


class BaseSimilarities(Generic[T]):
    def compute(self, query: T, candidates: List[T]) -> List[float]:
        ...

class BaseVectordatabase(Generic[T]):
    def __init__(self) -> None:
        ...

    def add(self, id: "BoxType", vector: T) -> None:
        ...

    def get(self, id: "BoxType") -> T:
        ...

    def get_many(self, ids: List["BoxType"]) -> List[T]:
        ...

    def get_smallest(self, query: T, top_k: int = 1) -> List[Tuple["BoxType", float]]:
        ...

    def delete(self, ids: List["BoxType"]) -> None:
        ...

    def save(self, path: Path) -> None:
        ...

    def load(self, path: Path) -> None:
        ...


BaseNumpyVectordatabase = BaseVectordatabase["NDArray"]
BaseTorchVectordatabase = BaseVectordatabase["Tensor"]