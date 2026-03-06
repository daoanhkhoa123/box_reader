from src.domain.entities import ImageInfo, BoxInfo
from typing import Optional

class BoxReader:
    version: str 
    """
    Determines whether readable information exists on a box.
    """

    def read(self, raw_bytes: bytes, image: Optional[ImageInfo] = None) -> BoxInfo:
        raise NotImplementedError