import logging

from src.computer_vision.box_detector.cv_box_detector import CVBoxDetector
from src.config.logging import setup_logging
from src.infrastructure.camera.cv_camera_stream import CVCameraStream
from src.services.box_detect_service import BoxDetectService
from src.services.image_reader_service import ImageReaderService

logger = logging.getLogger(__name__)

def main():
    setup_logging()

    reader = ImageReaderService([
        CVCameraStream(0),
        CVCameraStream(1),
    ])

    box_detector = CVBoxDetector()
    detector = BoxDetectService(box_detector)

    reader.start()

    for frames in reader.frames():
        detector.detect(frames)

if __name__ == "__main__":
    main()