from typing import Optional

from src.domain.entities import BoxInfo, ImageInfo


class BoxReader:
    version: str 
    """
    Determines whether readable information exists on a box.
    """

    def read(self, raw_bytes: bytes, image: Optional[ImageInfo] = None) -> BoxInfo:
        raise NotImplementedError