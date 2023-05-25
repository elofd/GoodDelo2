"""
Утилиты для работы с задачами
"""
from datetime import datetime

from app.models.database import database
from app.models.tasks import tasks_table
from app.models.users import users_table
from app.schemas import tasks as task_schema
from sqlalchemy import desc, func, select


async def create_task(task: task_schema.TaskModel, user):
    """
    Создаём задачу в БД
    :param task: Модель задачи
    :param user: залогиненый юзер
    :return: возвращаем задачу
    """
    query = (
        tasks_table.insert()
        .values(
            title=task.title,
            content=task.description,
            user_id=user["id"],
        )
        .returning(
            tasks_table.c.id,
            tasks_table.c.title,
            tasks_table.c.description,
        )
    )
    task = await database.fetch_one(query)

    task = dict(zip(task, task.values()))
    task["user_name"] = user["username"]
    return task


async def get_task(task_id: int):
    """
    Получаем информацию про задачу из БД
    :param task_id: номер задачи
    :return: возвращаем задачу
    """
    query = (
        select(
            [
                tasks_table.c.id,
                tasks_table.c.title,
                tasks_table.c.description,
                tasks_table.c.user_id,
                users_table.c.username.label("user_name"),
            ]
        )
        .select_from(tasks_table.join(users_table))
        .where(tasks_table.c.id == task_id)
    )
    return await database.fetch_one(query)


async def get_tasks(page: int):
    """
    Получаем список задач из БД
    :param page: максимальное количество задач на странице 10
    :return: возвращаем список задач
    """
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                tasks_table.c.id,
                tasks_table.c.title,
                tasks_table.c.description,
                tasks_table.c.user_id,
                users_table.c.username.label("user_name"),
            ]
        )
        .select_from(tasks_table.join(users_table))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_tasks_count():
    query = select([func.count()]).select_from(tasks_table)
    return await database.fetch_val(query)


async def update_task(task_id: int, task: task_schema.TaskModel):
    """
    Изменяем задачу в БД
    :param task_id: номер задачи
    :param task: Модель задачи
    :return: изменяем задачу в БД
    """
    query = (
        tasks_table.update()
        .where(tasks_table.c.id == task_id)
        .values(title=task.title, description=task.description)
    )
    return await database.execute(query)