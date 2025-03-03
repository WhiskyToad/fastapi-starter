from typing import Optional
from fastapi import HTTPException


class CustomError(HTTPException):
    def __init__(self, status_code: int, message: str, code: Optional[str] = None):
        super().__init__(status_code, detail=[{"message": message, "code": code}])
