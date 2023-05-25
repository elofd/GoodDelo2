"""
Маршруты для tasks
"""
from app.schemas.tasks import TaskDetailsModel, TaskModel
from app.schemas.users import User
from app.utils import tasks as task_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()


@router.post("/tasks", response_model=TaskDetailsModel, status_code=201)
async def create_task(task: TaskModel, current_user: User = Depends(get_current_user)):
    """
    Создаём новую задачу
    :param task: Модель задачи
    :param current_user: Текущий пользователь
    :return: Записываем задачу в БД
    """
    task = await task_utils.create_task(task, current_user)
    return task


@router.get("/tasks")
async def get_tasks(page: int = 1):
    """
    Выводим список задач
    :param page:
    :return: Возвращаем словарь с задачами
    """
    total_count = await task_utils.get_tasks_count()
    tasks = await task_utils.get_tasks(page)
    return {"total_count": total_count, "results": tasks}


@router.get("/tasks/{task_id}", response_model=TaskDetailsModel)
async def get_task(task_id: int):
    """
    Выводим детали конкретной задачи
    :param task_id: номер задачи
    :return: получаем информацию о задаче
    """
    return await task_utils.get_task(task_id)


@router.put("/tasks/{task_id}", response_model=TaskDetailsModel)
async def update_task(task_id: int, task_data: TaskModel, current_user=Depends(get_current_user)):
    """
    Изменяем задачу
    :param task_id: номер задачи
    :param task_data: модель задачи
    :param current_user: текущий пользователь
    :return: изменение задачи в БД
    """
    task = await task_utils.get_task(task_id)
    if task["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет доступа изменять эту задачу",
        )
    await task_utils.update_task(task_id=task_id, task=task_data)
    return await task_utils.get_task(task_id)


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user=Depends(get_current_user)):
    """
    Удаление задачи
    :param task_id: номер задачи
    :param current_user: текущий пользователь
    :return: удаление задачи из БД
    """
    task = await task_utils.get_task(task_id)
    if task["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет доступа удалять эту задачу",
        )
    await task_utils.delete_task(task_id=task_id)
    return {"detail": "Задача успешно удалена"}