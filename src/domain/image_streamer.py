from dataclasses import dataclass
from typing import List, Union

import cv2


@dataclass
class Frame:
    img: cv2.typing.MatLike
    src: str

Frames = List[Frame]

class ImageStreamer:
    def __init__(self, src: Union[int, str]) -> None:
        self.src = src
        self.camera = None

    def open(self) -> cv2.VideoCapture:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc, tb):
        self.close()