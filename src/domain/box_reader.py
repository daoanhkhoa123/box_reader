from src.domain.entities import Image, BoxInformation
from typing import Optional

class BoxReader:
    version: str 
    """
    Determines whether readable information exists on a box.
    """

    def read(self, raw_bytes: bytes, image: Optional[Image] = None) -> BoxInformation:
        raise NotImplementedError