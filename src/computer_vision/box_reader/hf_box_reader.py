import io
from PIL import Image as PILImage
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from typing import Optional
from src.domain.box_reader import BoxReader
from src.domain.entities import BoxInformation, Image


class HFBoxReader(BoxReader):
    version = "trocr-base-printed-v1"

    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained(
            "microsoft/trocr-base-printed"
        )
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-printed"
        )
        self.model.eval()

    def read(self, raw_bytes: bytes, image: Optional[Image] = None) -> BoxInformation:
        # Decode raw bytes into image
        pil_image = PILImage.open(io.BytesIO(raw_bytes)).convert("RGB")

        # Preprocess
        pixel_values = self.processor(
            images=pil_image, return_tensors="pt"
        ).pixel_values

        # OCR inference
        with torch.no_grad():
            generated_ids = self.model.generate(pixel_values)

        text = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0].strip()

        confidence = 1.0 if text else 0.0  # HF TrOCR doesn't expose token probs cleanly

        return BoxInformation(
            text=text,
            confidence=confidence
        )