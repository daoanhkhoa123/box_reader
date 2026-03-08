import logging
from typing import TYPE_CHECKING

import cv2

from src.domain.box_detector import BoxDetector
from src.domain.entities import ImageInfo
from src.domain.image_streamer import Frames

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.domain.unit_of_work import BaseUnitOfWorkFactory

from src.services.common import default_injection


def _lazy_boxdectect():
    from tests.mocks.boxes import MockBoxDetector
    return MockBoxDetector()

def _lazy_uowfact():
    from tests.mocks.repositories import (MockImageRepository,
                                          MockInferenceRepository)
    from tests.mocks.unit_of_work import MockUnitOfWorkFactory
    return MockUnitOfWorkFactory(MockImageRepository(), MockInferenceRepository())

_DEFAULT_PARAMS = {
    "box_detector": _lazy_boxdectect,
    "uow": _lazy_uowfact
}

@default_injection(_DEFAULT_PARAMS)
class BoxDetectService:
    def __init__(self, box_detector:BoxDetector, uow: "BaseUnitOfWorkFactory") -> None:
        self.box_detector = box_detector
        self.uow = uow
        self.logger = logger.getChild(self.__class__.__name__)
        self.logger.debug("Box Detect Service initialized with version %s", box_detector.version)

    def detect(self, frames: Frames):
        frame = frames[0].img # example    
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            raise Exception()
        
        raw_bytes = buffer.tobytes()

        has_box = self.box_detector.has_box(raw_bytes)
        paths = []

        if has_box:
            self.logger.debug("Box detected!")

            with self.uow() as uow:
                paths = [uow.image_repository.save(ImageInfo(f.src), f.img.tobytes()) for f in frames]

            self.logger.debug("Box image saved at %s", paths)   

        return has_box, paths