"""
Зависимости
"""
from app.utils import users as users_utils
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/register")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Получение текущего пользователя по токену
    :param token: токен
    :return: возвращаем пользователя
    """
    user = await users_utils.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
