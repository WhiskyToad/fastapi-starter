from sqlalchemy import Integer, String
from app.shared.models.BaseModel import EntityMeta
from sqlalchemy.orm import mapped_column


class UserModel(EntityMeta):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, index=True)
    username = mapped_column(String, index=True)
    hashed_password = mapped_column(String)
