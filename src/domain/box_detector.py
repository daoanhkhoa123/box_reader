from typing import Optional

from src.domain.entities import ImageInfo


class BoxDetector:
    version: str
    """
    Determines whether a box is present in an image.
    """

    def has_box(self, raw_bytes: bytes, image: Optional[ImageInfo] = None) -> bool:
        raise NotImplementedError