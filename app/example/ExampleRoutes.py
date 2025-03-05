from fastapi import Depends, APIRouter
from app.Example.ExampleService import ExampleService
from app.Example.ExampleSchema import Example

ExampleRouter = APIRouter(prefix="/api/example", tags=["example"])


@ExampleRouter.get("/", response_model=Example)
async def get_example(
    example_service: ExampleService = Depends(ExampleService),
):
    return await example_service.get_example()


@ExampleRouter.post("/", response_model=Example, status_code=201)
async def create_example(
    example: Example,
    example_service: ExampleService = Depends(ExampleService),
):
    return await example_service.create_example(example)


@ExampleRouter.put("/{example_id}", response_model=Example)
async def update_example(
    example_id: int,
    example: Example,
    example_service: ExampleService = Depends(ExampleService),
):
    return await example_service.update_example(example_id, example)


@ExampleRouter.delete("/{example_id}")
async def delete_example(
    example_id: int,
    example_service: ExampleService = Depends(ExampleService),
):
    return await example_service.delete_example(example_id)
