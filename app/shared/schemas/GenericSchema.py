from pydantic import BaseModel


class SuccessMessage(BaseModel):
    success: bool
