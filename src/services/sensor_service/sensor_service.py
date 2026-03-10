from src.domain.sensor import Sensor
from src.infrastructure.event_bus import EventBus
from dataclasses import dataclass

@dataclass
class SensorEvent:
    positive: bool = True

class SensorService:
    def __init__(self, sensor: Sensor, event_bus: EventBus) -> None:
        self.sensor = sensor
        self.event_bus = event_bus

    def poll(self) -> None:
        """
        Check sensor state and emit events.
        This should be called repeatedly by the main loop.
        """

        if self.sensor.positive_change():
            self.event_bus.emit(SensorEvent(positive=True))

        if self.sensor.negative_change():
            self.event_bus.emit(SensorEvent(positive=False))

        