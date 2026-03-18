from src.domain.sensor import Sensor
from src.infrastructure.camera.cv_camera_stream import CVCameraStream
from src.infrastructure.event_bus import EventBus
from src.services.cvllm_bigbox_service import CVLLMBigBoxSevice
from src.services.sensor_service import SensorService


def bootstrap():

    # infrastructure
    bus = EventBus()

    camera = CVCameraStream(0)

    # domain
    sensor = Sensor()

    # services
    sensor_service = SensorService(sensor, bus)

    cvllm_bigbox_service = CVLLMBigBoxSevice(bus)

    return sensor_service


def main():

    sensor_service = bootstrap()

    sensor_service.run()


if __name__ == "__main__":
    main()