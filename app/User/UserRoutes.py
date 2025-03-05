from fastapi import Depends, APIRouter
from app.Auth.auth_utils import get_user_id_from_token
from app.User.UserService import UserService
from app.User.UserSchema import UserChangePassword, UserEditProfile, UserSignup, User
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.Jwt.JwtSchema import Token
from app.Auth.AuthService import AuthService


UserRouter = APIRouter(prefix="/api/user", tags=["user"])


@UserRouter.post("/", response_model=Token, status_code=201)
async def signup(
    user_details: UserSignup, user_service: UserService = Depends(UserService)
):
    token = await user_service.signup(user_details)
    return token


@UserRouter.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.login(form_data.username, form_data.password)


@UserRouter.get("/me", response_model=User)
async def read_users_me(
    user_id: int = Depends(get_user_id_from_token),
    user_service: UserService = Depends(UserService),
):
    return user_service.get_current_user(user_id)


@UserRouter.put("/me", response_model=User)
async def edit_user_profile(
    updated_details: UserEditProfile,
    user_id: int = Depends(get_user_id_from_token),
    user_service: UserService = Depends(UserService),
):
    return await user_service.edit_user_profile(updated_details, user_id)


@UserRouter.put("/me/password", response_model=dict)
async def change_user_password(
    password_details: UserChangePassword,
    user_id: int = Depends(get_user_id_from_token),
    user_service: UserService = Depends(UserService),
):
    result = await user_service.change_user_password(password_details, user_id)
    return {"result": result}
