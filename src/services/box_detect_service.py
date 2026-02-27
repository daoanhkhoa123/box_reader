import cv2
from src.domain.box_detector import BoxDetector
from src.domain.image_stream import Frames

import logging
logger = logging.getLogger(__name__)

###########
# Could add image storage when seen or event emmiter to other service
###############
class BoxDetectService:
    def __init__(self, box_detector:BoxDetector) -> None:
        self.box_detector = box_detector
        self.logger = logger.getChild(self.__class__.__name__)
        self.logger.debug("Box Detect Service initialized")

    def detect(self, frames: Frames):
        frame = frames[0] # example    
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            raise Exception()
        
        raw_bytes = buffer.tobytes()

        has_box = self.box_detector.has_box(raw_bytes)

        if has_box:
            self.logger.debug("Box detected!")