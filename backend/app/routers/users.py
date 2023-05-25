"""
Маршруты для users
"""
from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Страница логина
    :param form_data: проверка пароля
    :return: логиним пользователя, создаём ему токен
    """
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    return await users_utils.create_user_token(user_id=user["id"])


@router.post("/register", response_model=users.User)
async def create_user(user: users.UserCreate):
    """
    Регистрация нового пользователя
    :param user: модель нового пользователя
    :return: создаём нового пользователя в БД
    """
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return await users_utils.create_user(user=user)


@router.post("/logout")
async def logout(current_user: users.User = Depends(get_current_user)):
    """
    Логаут текущего пользователя
    :param current_user: текущий пользователь
    :return: выходим, удаляем токен
    """
    return await users_utils.revoke_user_token(token=current_user.token)
