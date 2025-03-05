from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.shared.config.env_variables import ALGORITHM, SECRET_KEY
from app.shared.errors.CustomError import CustomError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise CustomError(status_code=401, message="No user found")
    except JWTError:
        raise CustomError(status_code=400, message="JWT Error")
    return int(user_id)
