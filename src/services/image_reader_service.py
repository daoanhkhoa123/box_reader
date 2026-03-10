# import logging
# from typing import Iterator, List

# import cv2

# from src.domain.image_streamer import Frames, ImageStreamer, Frame
# from src.services.common import default_injection

# logger = logging.getLogger(__name__)

# def _lazy_loader():
#     from src.infrastructure.camera.cv_camera_stream import CVCameraStream
#     return [CVCameraStream(0)]

# _DEFAULT_PARAMS = {
#     "cameras": _lazy_loader,
# }

# @default_injection(_DEFAULT_PARAMS)
# class ImageReaderService:
#     def __init__(self, cameras: List[ImageStreamer]) -> None:
#         self.cameras = cameras
#         self.captures: List[cv2.VideoCapture] = []
#         self.running = False

#     def start(self) -> None:
#         logger.info("Starting image reader service")
#         self.captures = [camera.open() for camera in self.cameras]
#         self.running = True

#     def frames(self) -> Iterator[Frames]:
#         if not self.running:
#             raise RuntimeError("ImageReaderService not started")

#         try:
#             while self.running:
#                 batch = []

#                 for idx, cap in enumerate(self.captures):
#                     ok, frame = cap.read()
#                     if not ok:
#                         logger.error("Failed to read frame from camera %d", idx)
#                         raise RuntimeError("Camera read failure")

#                     batch.append(Frame(frame, str(self.cameras[idx].src)))

#                 yield batch  # one frame per camera

#         finally:
#             self.stop()

#     def stop(self) -> None:
#         logger.info("Stopping image reader service")
#         for camera in self.cameras:
#             camera.close()

#         self.captures.clear()
#         self.running = False