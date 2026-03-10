from dataclasses import dataclass
from typing import List, Union
from typing_extensions import Self

import cv2

Image = cv2.typing.MatLike

class Frame:
    img: cv2.typing.MatLike
    src: str

Frames = List[Frame]

class ImageStreamer:
    _instance = {}
    def __new__(cls, src: Union[int, str], *args, **kwargs) -> Self:
        key = (cls.__name__, src)
        if key not in cls._instance:
            instance = super().__new__(cls)
            cls._instance[key] = instance
        return cls._instance[key]

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