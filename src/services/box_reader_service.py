from src.domain.box_reader import BoxReader
from src.domain.image_stream import Frames
from src.domain.entities import BoxInfo

class BoxReaderService:
    def read(self, frames: Frames) -> BoxInfo:
        ...