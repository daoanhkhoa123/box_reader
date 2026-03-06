from typing_extensions import Self

from src.domain.repositories import ImageRepository, InferenceRepository


class BaseUnitOfWork:
    image_repository: ImageRepository
    inference_repository: InferenceRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.rollback()

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class BaseUnitOfWorkFactory:
    def __call__(self) -> BaseUnitOfWork:
        raise NotImplementedError
