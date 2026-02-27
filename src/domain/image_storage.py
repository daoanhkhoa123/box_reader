from pathlib import Path
from src.domain.entities import Image


class ImageStorage:
    """
    Stores raw image frames for training and auditing.
    """

    def save(self, image: Image, raw_bytes: bytes) -> Path:
        raise NotImplementedError

    def load(self, path: Path) -> bytes:
        raise NotImplementedError