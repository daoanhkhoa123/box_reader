from src.domain.repositories import ImageRepository, InferenceRepository
from src.domain.unit_of_work import BaseUnitOfWork, BaseUnitOfWorkFactory


class MockUnitOfWork(BaseUnitOfWork):
    def __init__(
        self,
        image_repository: ImageRepository,
        inference_repository: InferenceRepository,
    ) -> None:
        self.image_repository = image_repository
        self.inference_repository = inference_repository

        self.committed: bool = False
        self.rolled_back: bool = False

    def __enter__(self):
        return super().__enter__()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    
class MockUnitOfWorkFactory(BaseUnitOfWorkFactory):
    def __init__(self, image_repository: ImageRepository,
        inference_repository: InferenceRepository) -> None:
        self.image_repository = image_repository
        self.inference_repository = inference_repository

    def __call__(self) -> MockUnitOfWork:
        return MockUnitOfWork(self.image_repository, self.inference_repository)
