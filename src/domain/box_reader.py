from typing import Optional, Tuple

from src.domain.entities import BoxInfo, ImageInfo


class BoxReader:
    version: str 
    """
    Determines whether readable information exists on a box.
    """

    def read(self, raw_bytes: bytes, image: Optional[ImageInfo] = None) -> Tuple[float, BoxInfo]:
        raise NotImplementedError