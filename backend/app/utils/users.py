"""
Утилиты для пользователей
"""
import hashlib
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import and_

from app.models.database import database
from app.models.users import tokens_table, users_table
from app.schemas import users as user_schema


def get_random_string(length=12):
    """
    Получаем рандомную строку
    :param length: из 12 символов
    :return: возвращаем рандомную строку
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """
    Хэшируем пароль
    :param password: пароль
    :param salt: сюда записываем рандомную строку
    :return: возвращаем захешированный пароль
    """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """
    Проверка пароля
    :param password: пароль
    :param hashed_password: захешированный пароль
    :return: вовращаем True, если пароли совпали
    """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    """
    Получаем пользователей по email
    :param email: email
    :return: возвращаем список пользователей из БД
    """
    query = users_table.select().where(users_table.c.email == email)
    return await database.fetch_one(query)


async def create_user(user: user_schema.UserCreate):
    """
    Создаём пользователя
    :param user: Модель для создания пользователя
    :return: возвращаем словарь с данными пользователя
    """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email, username=user.username, hashed_password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "token": token_dict}


async def create_user_token(user_id: int):
    """
    Создаём токен для пользователя
    :param user_id: номер пользователя
    :return: Возвращаем токен из БД
    """
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )

    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    """
    Получаем пользователя по токену
    :param token: токен
    :return: возвращаем пользователя из БД
    """
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)
