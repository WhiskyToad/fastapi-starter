from fastapi import Depends
from app.User.UserRepository import UserRepository
from app.User.UserModel import UserModel
from app.User.UserSchema import User, UserChangePassword, UserEditProfile, UserSignup
from app.Jwt.JwtService import JwtService
from app.Auth.security import SecurityUtils
from app.shared.errors.CustomError import CustomError
from app.Auth.AuthService import AuthService
from app.Jwt.JwtSchema import Token


class UserService:
    user_repository: UserRepository
    security_utils: SecurityUtils
    jwt_service: JwtService
    auth_service: AuthService

    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        security_utils: SecurityUtils = Depends(SecurityUtils),
        jwt_service: JwtService = Depends(JwtService),
        auth_service: AuthService = Depends(AuthService),
    ) -> None:
        self.user_repository = user_repository
        self.security_utils = security_utils
        self.jwt_service = jwt_service
        self.auth_service = auth_service

    def _find_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise CustomError(status_code=400, message="No user found")
        return user

    async def signup(
        self,
        user_details: UserSignup,
    ) -> Token:
        existing_user = self.user_repository.get_user_by_email(user_details.email)
        if existing_user:
            raise CustomError(
                status_code=400, message="Email already exists", code="email"
            )
        hashed_password = self.security_utils.get_password_hash(user_details.password)
        self.user_repository.create(
            UserModel(
                email=user_details.email,
                hashed_password=hashed_password,
                username=user_details.username,
            )
        )
        token = await self.auth_service.login(user_details.email, user_details.password)
        return token

    def get_current_user(self, user_id: int) -> User:
        user = self._find_user_by_id(user_id)
        return User(email=user.email, id=user.id, username=user.username)

    async def edit_user_profile(
        self, new_details: UserEditProfile, user_id: int
    ) -> User:
        user = await self.user_repository.edit_user_profile(new_details, user_id)
        if user is None:
            raise CustomError(status_code=400, message="No user found")
        return User(email=user.email, id=user.id, username=user.username)

    async def change_user_password(
        self, password_details: UserChangePassword, user_id: int
    ) -> bool:
        user = self._find_user_by_id(user_id)
        password_check = self.security_utils.verify_password(
            password_details.current_password, user.hashed_password
        )
        if not password_check:
            raise CustomError(status_code=400, message="Password is incorrect")
        hashed_password = self.security_utils.get_password_hash(
            password_details.new_password
        )
        return await self.user_repository.change_password(hashed_password, user_id)
