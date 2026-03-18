import logging
import os
from dataclasses import dataclass
from typing import Union

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoModel, AutoImageProcessor


@dataclass
class DinoV3ModelConfig:
    model_path: str = "weights/dinov3"
    device: str = "cpu"


class DinoV3Model:
    def __init__(self, config: DinoV3ModelConfig):
        self.model_path = config.model_path
        self.device = config.device

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(
            "init: model_path=%s device=%s",
            self.model_path, self.device
        )

        self._load_model()

    # -------------------------
    # Lifecycle
    # -------------------------
    def _load_model(self):
        self.logger.debug("enter: load_model")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(self.model_path)

        self.processor = AutoImageProcessor.from_pretrained(self.model_path)
        self.model = AutoModel.from_pretrained(self.model_path)

        self.model.to(self.device)
        self.model.eval()

        self.logger.info("Model loaded from %s", self.model_path)
        self.logger.debug("exit: load_model")

    # -------------------------
    # Preprocess
    # -------------------------
    def _decode_image(self, image: Union[bytes, np.ndarray, str]) -> Image.Image:
        self.logger.debug("enter: decode_image type=%s", type(image))

        if isinstance(image, bytes):
            arr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Invalid image bytes")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

        elif isinstance(image, str):
            img = Image.open(image).convert("RGB")

        elif isinstance(image, np.ndarray):
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

        else:
            raise TypeError(f"Unsupported image type: {type(image)}")

        self.logger.debug("exit: decode_image")
        return img

    # -------------------------
    # Inference
    # -------------------------
    @torch.no_grad()
    def embed(self, image: Union[bytes, np.ndarray, str]) -> np.ndarray:
        self.logger.debug("enter: embed")

        img = self._decode_image(image)
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)

        outputs = self.model(**inputs)

        # 👇 best practice: use pooled output (CLS)
        embedding = outputs.pooler_output.cpu().numpy()[0]

        self.logger.info("Embedding shape: %s", embedding.shape)
        self.logger.debug("exit: embed")

        return embedding

    # -------------------------
    # Utility
    # -------------------------
    def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        self.logger.debug("enter: similarity")

        emb1 = emb1 / np.linalg.norm(emb1)
        emb2 = emb2 / np.linalg.norm(emb2)

        score = float(np.dot(emb1, emb2))

        self.logger.debug("exit: similarity score=%f", score)
        return score