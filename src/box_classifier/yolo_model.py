import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Union

import cv2
import numpy as np
from ultralytics import YOLO


@dataclass
class YoloModelConfig:
    model_path: str = "yolov8n.pt"
    device: str = "cpu"
    conf_threshold: float = 0.25

class YoloModel:
    def __init__(self, config: YoloModelConfig):
        self.model_path = config.model_path
        self.device = config.device
        self.conf_threshold = config.conf_threshold

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("init: model_path=%s device=%s", self.model_path, self.device)

        self._load_model()

    def _load_model(self):
        self.model = YOLO(self.model_path)
        self.model.to(self.device)

        self.logger.info("Model loaded: %s", self.model_path)

    def _decode_image(self, image: Union[bytes, np.ndarray, str]) -> np.ndarray:
        self.logger.debug("enter: decode_image type=%s", type(image))

        if isinstance(image, bytes):
            arr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        elif isinstance(image, str):
            img = cv2.imread(image)

        elif isinstance(image, np.ndarray):
            img = image

        else:
            raise TypeError(f"Unsupported image type: {type(image)}")

        if img is None:
            self.logger.error("Failed to decode image")
            raise ValueError("Invalid image input")

        self.logger.debug("exit: decode_image shape=%s", img.shape)
        return img

    def predict(self, image: Union[bytes, np.ndarray, str]) -> List[Dict[str, Any]]:
        self.logger.debug("enter: predict")

        img = self._decode_image(image)

        results = self.model(img, conf=self.conf_threshold)

        detections = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                detections.append({
                    "class_id": int(box.cls),
                    "confidence": float(box.conf),
                    "bbox": box.xyxy.tolist()[0],  # [x1, y1, x2, y2]
                })

        self.logger.info("Detected %d objects", len(detections))
        self.logger.debug("exit: predict")

        return detections

    def has_object(self, image: Union[bytes, np.ndarray, str]) -> bool:
        self.logger.debug("enter: has_object")

        detections = self.predict(image)
        result = len(detections) > 0

        self.logger.debug("exit: has_object result=%s", result)
        return result