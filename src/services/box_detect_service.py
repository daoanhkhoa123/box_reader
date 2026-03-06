import cv2
from src.domain.box_detector import BoxDetector
from src.domain.image_streamer import Frames
from typing import TYPE_CHECKING
from src.domain.entities import ImageInfo

import logging
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.domain.unit_of_work import BaseUnitOfWorkFactory

###########
# Could add image storage when seen or event emmiter to other service
###############
class BoxDetectService:
    def __init__(self, box_detector:BoxDetector, uow: "BaseUnitOfWorkFactory") -> None:
        self.box_detector = box_detector
        self.uow = uow
        self.logger = logger.getChild(self.__class__.__name__)
        self.logger.debug("Box Detect Service initialized")

    def detect(self, frames: Frames):
        frame = frames[0] # example    
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            raise Exception()
        
        raw_bytes = buffer.tobytes()

        has_box = self.box_detector.has_box(raw_bytes)
        paths = []

        if has_box:
            with self.uow() as uow:
                paths = [uow.image_repository.save(ImageInfo(), f.tobytes()) for f in frames]
                
            self.logger.debug("Box detected!")

        return has_box, paths