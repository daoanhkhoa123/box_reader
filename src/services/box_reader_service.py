import logging
from typing import TYPE_CHECKING, Tuple

from src.domain.box_reader import BoxReader
from src.domain.entities import BoxInfo, ImageInfo, InferenceResult
from src.domain.image_streamer import Frames

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

    def read(self, frames: Frames, image_id: str) -> Tuple[BoxInfo, InferenceResult]:
        box_info = self.box_reader.read(frames[0].img.tobytes())
        with self.uow() as uow:
            inference_result = InferenceResult(image_id, box_information=box_info, model_version=self.box_reader.version)
            inference_result = uow.inference_repository.save(inference_result)

        return box_info, inference_result