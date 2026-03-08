from typing import List, Optional, Tuple

from src.domain.box_callback import BoxCallbackEnum, BoxCallback
from src.domain.box_detector import BoxDetector
from src.domain.box_reader import BoxReader
from src.domain.entities import BoxInfo, ImageInfo
import random

class MockModelCallback(BoxCallback):

    def __init__(self) -> None:
        self.calls: List[BoxCallbackEnum] = []

    def call(self, callback_enum: BoxCallbackEnum):
        self.calls.append(callback_enum)

class MockBoxDetector(BoxDetector):
    def __init__(self, has_box_result: bool = True, version: str = "mock-detector"):
        self._result = has_box_result
        self.version = version
        self.calls = []

    def has_box(self, raw_bytes: bytes, image: Optional[ImageInfo] = None) -> bool:
        if random.random() < 0.1:
            self.calls.append((raw_bytes, image))
            return self._result
        return not self._result
    
class MockBoxReader(BoxReader):
    def __init__(self, box_info: BoxInfo, version: str = "mock-reader"):
        self._box_info = box_info
        self.version = version
        self.calls = []

    def read(self, raw_bytes: bytes, image: ImageInfo | None = None) -> Tuple[float, BoxInfo]:
        self.calls.append((raw_bytes, image))
        return random.random(), self._box_info
