from fastapi import Depends
from app.User.UserRepository import UserRepository
from typing import Type
from app.Auth.security import SecurityUtils
from app.Jwt.JwtSchema import Token
from datetime import timedelta
from app.Jwt.JwtService import JwtService
from app.shared.errors.CustomError import CustomError


class AuthService:
    user_repository: UserRepository
    security_utils: SecurityUtils
    jwt_service: JwtService

    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        security_utils: SecurityUtils = Depends(SecurityUtils),
        jwt_service: JwtService = Depends(JwtService),
    ) -> None:
        self.user_repository = user_repository
        self.security_utils = security_utils
        self.jwt_service = jwt_service

    async def login(self, username: str, password: str) -> Token:
        user = self.authenticate_user(username, password)
        if not user:
            raise CustomError(
                status_code=400,
                message="Incorrect email or password",
            )
        access_token_expires = timedelta(minutes=30)
        access_token = self.jwt_service.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    def authenticate_user(
        self,
        email: str,
        password: str,
    ):
        # Call repository to get user
        user = self.user_repository.get_user_by_email(email)

        # Validate credentials
        if not user or not self.security_utils.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return False

        return user
