from src.domain.entities import ImageInfo
from typing import Iterable
from src.domain.entities import InferenceResult

class InferenceRepository:
    """
    Stores inference results for analysis and retraining.
    """

    def save(self, result: InferenceResult) -> InferenceResult:
        raise NotImplementedError

    def list_by_image(self, image_id: str) -> Iterable[InferenceResult]:
        raise NotImplementedError

class ImageRepository:
    """
    Stores raw image frames for training and auditing.
    """

    def save(self, image: ImageInfo, raw_bytes: bytes) -> str:
        raise NotImplementedError

    def read(self, path: str) -> bytes:
        raise NotImplementedError