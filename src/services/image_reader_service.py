import cv2
import logging
from typing import List, Iterator
from src.domain.image_stream import Frames
from src.domain.image_stream import ImageStream

logger = logging.getLogger(__name__)


class ImageReaderService:
    def __init__(self, cameras: List[ImageStream]) -> None:
        self._cameras = cameras
        self._captures: List[cv2.VideoCapture] = []
        self._running = False

    def start(self) -> None:
        logger.info("Starting image reader service")
        self._captures = [camera.open() for camera in self._cameras]
        self._running = True

    def frames(self) -> Iterator[Frames]:
        if not self._running:
            raise RuntimeError("ImageReaderService not started")

        try:
            while self._running:
                batch = []

                for idx, cap in enumerate(self._captures):
                    ok, frame = cap.read()
                    if not ok:
                        logger.error("Failed to read frame from camera %d", idx)
                        raise RuntimeError("Camera read failure")

                    batch.append(frame)

                yield batch  # one frame per camera

        finally:
            self.stop()

    def stop(self) -> None:
        logger.info("Stopping image reader service")
        for camera in self._cameras:
            camera.close()

        self._captures.clear()
        self._running = False