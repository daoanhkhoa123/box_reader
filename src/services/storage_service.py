from src.domain.result_storage import ResultStorage
from src.domain.image_storage import ImageStorage
from src.domain.entities import ImageInfo

class StorageService:
    def __init__(self, image_storage: ImageStorage, result_storage: ResultStorage) -> None:
        self.image_storage = image_storage
        self.result_storage = result_storage

    def save_image(self, image: ImageInfo, bytes: bytes) -> str:
        return self.image_storage.save(image, bytes)
    
    def read_image(self, path: str) -> bytes:
        return self.image_storage.read(path)