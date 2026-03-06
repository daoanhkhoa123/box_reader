from src.domain.box_reader import BoxReader
from src.domain.image_streamer import Frames
from src.domain.entities import BoxInfo
from typing import TYPE_CHECKING, Tuple
from src.domain.entities import ImageInfo, InferenceResult

import logging
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.domain.unit_of_work import BaseUnitOfWorkFactory

class BoxReaderService:
    def __init__(self, box_reader: BoxReader, uow:"BaseUnitOfWorkFactory") -> None:
        self.box_reader = box_reader
        self.uow = uow

    def read(self, frames: Frames) -> Tuple[BoxInfo, InferenceResult]:
        box_info = self.box_reader.read(frames)
        with self.uow() as uow:
            inference_result = InferenceResult(box_information=box_info)
            inference_result = uow.inference_repository.save(inference_result)

        return box_info, inference_result