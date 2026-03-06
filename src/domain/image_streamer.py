import cv2
from typing import Union, List

Frame = cv2.typing.MatLike
Frames = List[Frame]


class ImageStreamer:
    """
    Interface / base class for camera streams.
    Implementations should return cv2.VideoCapture in __enter__.
    """

    def __init__(self, src: Union[int, str]) -> None:
        self.src = src
        self.camera = None

    def open(self) -> cv2.VideoCapture:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
