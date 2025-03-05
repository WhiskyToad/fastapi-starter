from typing import Optional
from fastapi import Depends
from app.User.UserModel import UserModel
from sqlalchemy.orm import Session
from app.User.UserSchema import UserEditProfile
from app.shared.config.Database import get_db_connection


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    async def edit_user_profile(
        self, new_details: UserEditProfile, user_id: int
    ) -> UserModel | None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            return None
        user.email = new_details.email
        user.username = new_details.username
        self.db.commit()
        self.db.refresh(user)
        return user

    async def change_password(self, new_password: str, user_id: int) -> bool:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user is None:
            return False
        user.hashed_password = new_password
        self.db.commit()
        self.db.refresh(user)
        return True
