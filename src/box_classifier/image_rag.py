from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING
import numpy as np
from numpy.typing import NDArray
from src.box_classifier.vector_database.base import BaseVectordatabase
from src.box_classifier.yolo_model import YoloModel
from src.box_classifier.dino_model import DinoV3Model


if TYPE_CHECKING:
    from src.box_classifier.domains import BoxType
    from numpy.typing import NDArray

class ImageRag:
    def __init__(self, vector_db: BaseVectordatabase, yolo_model: YoloModel, dino_model: DinoV3Model) -> None:
        self._db = vector_db
        self._yolo = yolo_model
        self._dino = dino_model

    def _crop(self, image: np.ndarray, bbox: List[float]) -> np.ndarray:
        x1, y1, x2, y2 = map(int, bbox)
        return image[y1:y2, x1:x2]

    def embed(self, image: Union[bytes, np.ndarray, str]) -> List[NDArray]:
        img = self._yolo._decode_image(image)
        dets = self._yolo.predict(img)
        embs: List[NDArray] = []

        for d in dets:
            crop = self._crop(img, d["bbox"])
            emb = self._dino.embed(crop)
            embs.append(emb)
        return embs

    def retrieve(self, image: Union[bytes, np.ndarray, str], top_k: int = 3) -> List[Tuple[Any, float]]:
        embs = self.embed(image)
        results: List[Tuple["BoxType", float]] = self._db.get_smallest(embs, top_k)            
        return results