import logging
from typing import Optional, Union

import cv2

from src.domain.image_streamer import ImageStreamer

logger = logging.getLogger(__name__)


class CVCameraStream(ImageStreamer):
    def __init__(self, src: Union[int, str]) -> None:
        super().__init__(src)
        self.camera: Optional[cv2.VideoCapture] = None
        self.logger = logger.getChild(self.__class__.__name__)

    def open(self) -> cv2.VideoCapture:
        self.logger.info("Opening camera source: %s", self.src)

        self.camera = cv2.VideoCapture(self.src)

        if not self.camera.isOpened():
            self.logger.error("Cannot open camera: %s", self.src)
            raise RuntimeError(f"Cannot open camera {self.src}")

        return self.camera

    def close(self) -> None:
        if self.camera is not None:
            self.logger.info("Releasing camera source: %s", self.src)
            self.camera.release()
            self.camera = None