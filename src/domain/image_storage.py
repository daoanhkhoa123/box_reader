from src.domain.entities import ImageInfo


class ImageStorage:
    """
    Stores raw image frames for training and auditing.
    """

    def save(self, image: ImageInfo, raw_bytes: bytes) -> str:
        raise NotImplementedError

    def read(self, path: str) -> bytes:
        raise NotImplementedError