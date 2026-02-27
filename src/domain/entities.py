from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Image:
    """
    A synchronized image frame captured from a camera.
    """
    image_id: str
    camera_id: str
    captured_at: datetime
    storage_path: str 

@dataclass(frozen=True)
class BoxInformation:
    made_in: str 
    cost: str

    def to_propmt(self) -> str:
        return """{
            "made_in": "...",
            "cost": "..."
        }"""

@dataclass(frozen=True)
class Result:
    """
    Result of box reading for a given image.
    """
    image_id: str
    detected_at: datetime
    model_version: str
    box_information: BoxInformation

    