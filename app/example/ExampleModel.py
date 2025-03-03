from sqlalchemy import Integer, String
from app.shared.models.BaseModel import EntityMeta
from sqlalchemy.orm import mapped_column


class ExampleModel(EntityMeta):
    __tablename__ = "examples"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True)
