from fastapi import FastAPI, Request
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.example.ExampleRoutes import ExampleRouter

load_dotenv()

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    print(errors)
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {"message": error["msg"], "code": error["type"]} for error in errors
            ]
        },
    )


app.include_router(ExampleRouter)
