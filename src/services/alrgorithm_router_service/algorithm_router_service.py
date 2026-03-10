from src.domain.image_streamer import ImageStreamer, Image
from src.infrastructure.event_bus import EventBus
from typing import Dict

class AlgorithmRouterService:
    def __init__(self, camera:ImageStreamer, event_bus: EventBus, algorithm_register:Dict[str, str] ) -> None:
        self.event_bus = event_bus
        self.algo_register = algorithm_register

    def run(self):
        img : Image = Image()
        detection = self.detect(img)
        return self.algo_register[detection]

    def detect(self, image: Image) -> str:
        """
        Do some magic thing here
        """
        return str