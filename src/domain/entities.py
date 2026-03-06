from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ImageInfo:
    """
    A synchronized image frame captured from a camera.
    """
    camera_id: str
    captured_at: datetime = datetime.now()
    image_id: Optional[str] = None

@dataclass(frozen=True)
class BoxInfo:
    made_in: str 
    cost: str

    def to_propmt(self) -> str:
        return """{
            "made_in": "...",
            "cost": "..."
        }"""

@dataclass(frozen=True)
class InferenceResult:
    """
    Result of box reading for a given image.
    """
    image_id: str
    model_version: str
    box_information: BoxInfo

    