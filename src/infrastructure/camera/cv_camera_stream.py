import cv2
from src.domain.image_streamer import ImageStreamer
from typing import Optional, Union

class CVCameraStream(ImageStreamer):
    def __init__(self, src: Union[int, str]) -> None:
        super().__init__(src)
        self.src = src
        self.camera: Optional[cv2.VideoCapture] = None

    def open(self) -> cv2.VideoCapture:
        self.camera = cv2.VideoCapture(self.src)
        if not self.camera.isOpened():
            raise RuntimeError(f"Cannot open camera {self.src}")
        return self.camera

    def close(self) -> None:
        if self.camera is not None:
            self.camera.release()
            self.camera = None
