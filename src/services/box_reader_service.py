import logging
from typing import TYPE_CHECKING, Tuple

from src.domain.box_reader import BoxReader
from src.domain.entities import BoxInfo, InferenceResult
from src.domain.image_streamer import Frames
from src.domain.box_callback import BoxCallbackEnum

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.domain.unit_of_work import BaseUnitOfWorkFactory

from src.services.common import default_injection


def _lazy_boxreader():
    from tests.mocks.boxes import MockBoxReader
    return MockBoxReader(BoxInfo("test_made in", "69420"))

def _lazy_uowfact():
    from tests.mocks.repositories import (MockImageRepository,
                                          MockInferenceRepository)
    from tests.mocks.unit_of_work import MockUnitOfWorkFactory
    return MockUnitOfWorkFactory(MockImageRepository(), MockInferenceRepository())

_DEFAULT_PARAMS = {
    "box_reader": _lazy_boxreader,
    "uow": _lazy_uowfact
}

@default_injection(_DEFAULT_PARAMS)
class BoxReaderService:
    def __init__(self, box_reader: BoxReader, uow:"BaseUnitOfWorkFactory") -> None:
        self.box_reader = box_reader
        self.uow = uow
        self.logger = logger.getChild(self.__class__.__name__)
        self.logger.debug("Box Reader Service initialized with version %s", box_reader.version)

    def read(self, frames: Frames, image_id: str) -> Tuple[BoxCallbackEnum, InferenceResult]:
        confidence_score, box_info = self.box_reader.read(frames[0].img.tobytes())
        self.logger.debug("Box information extracted %s", box_info)

        with self.uow() as uow:
            inference_result = InferenceResult(image_id, box_information=box_info, model_version=self.box_reader.version)
            inference_result = uow.inference_repository.save(inference_result)
            self.logger.debug("Inference result saved image_id=%s", image_id)

        callback_enum = BoxCallbackEnum.NONE
        # NOTE: this is just not yet known for sure which should be done
        if confidence_score > 0.5:
            callback_enum = BoxCallbackEnum.ACCEPT
        else:
            callback_enum = BoxCallbackEnum.REJECT

        return callback_enum, inference_result