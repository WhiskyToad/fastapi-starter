from fastapi import Depends
from app.Example.ExampleRepository import ExampleRepository
from app.Example.ExampleModel import ExampleModel
from app.Example.ExampleSchema import Example
from app.shared.errors.CustomError import CustomError


class ExampleService:
    example_repository: ExampleRepository

    def __init__(
        self,
        example_repository: ExampleRepository = Depends(ExampleRepository),
    ) -> None:
        self.example_repository = example_repository

    def _find_example_by_id(self, example_id: int):
        example = self.example_repository.get_example_by_id(example_id)
        if example is None:
            raise CustomError(status_code=400, message="No example found")
        return example

    async def get_example(self) -> Example:
        # Implement logic to get default example or list of examples
        example = self.example_repository.get_example()
        if example is None:
            raise CustomError(status_code=400, message="No example found")
        return Example(
            name=example.name,
            id=example.id,
        )

    async def create_example(self, example: Example) -> Example:
        existing_example = self.example_repository.get_example_by_name(example.name)
        if existing_example:
            raise CustomError(
                status_code=400, message="Name already exists", code="name"
            )
        return self.example_repository.create(
            ExampleModel(
                name=example.name,
            )
        )

    async def update_example(self, example_id: int, example: Example) -> Example:
        existing_example = self._find_example_by_id(example_id)
        existing_example.name = example.name
        updated_example = self.example_repository.update(existing_example)
        return Example(name=updated_example.name, id=updated_example.id)

    async def delete_example(self, example_id: int):
        example = self._find_example_by_id(example_id)
        self.example_repository.delete(example)
        return {"message": "Example deleted successfully"}
