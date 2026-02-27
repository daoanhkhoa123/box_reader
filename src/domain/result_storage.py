from typing import Iterable
from src.domain.entities import InferenceResult


class ResultStorage:
    """
    Stores inference results for analysis and retraining.
    """

    def save(self, result: InferenceResult) -> None:
        raise NotImplementedError

    def list_by_image(self, image_id: str) -> Iterable[InferenceResult]:
        raise NotImplementedError