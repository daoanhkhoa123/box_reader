from typing import Dict, Iterable, List

from src.domain.entities import ImageInfo, InferenceResult
from src.domain.repositories import ImageRepository, InferenceRepository


class MockInferenceRepository(InferenceRepository):

    def __init__(self) -> None:
        self._data: Dict[str, List[InferenceResult]] = {}

    def save(self, result: InferenceResult) -> InferenceResult:
        image_id = result.image_id

        if image_id not in self._data:
            self._data[image_id] = []

        self._data[image_id].append(result)
        return result

    def list_by_image(self, image_id: str) -> Iterable[InferenceResult]:
        return list(self._data.get(image_id, []))



class MockImageRepository(ImageRepository):

    def __init__(self) -> None:
        self._images: Dict[str, bytes] = {}
        self._metadata: Dict[str, ImageInfo] = {}

    def save(self, image: ImageInfo, raw_bytes: bytes) -> str:
        idd = "test none holder" if image.image_id is None else image.image_id
        
        self._images[idd] = raw_bytes
        self._metadata[idd] = image

        return idd

    def read(self, path: str) -> bytes:
        if path not in self._images:
            raise KeyError(f"Image not found: {path}")

        return self._images[path]