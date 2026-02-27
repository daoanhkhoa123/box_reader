from src.domain.entities import Image
from typing import Optional


class BoxDetector:
    version: str
    """
    Determines whether a box is present in an image.
    """

    def has_box(self, raw_bytes: bytes, image: Optional[Image] = None) -> bool:
        raise NotImplementedError