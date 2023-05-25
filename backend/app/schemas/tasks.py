"""
Модели для задач
"""
from pydantic import BaseModel


class TaskModel(BaseModel):
    """
    Модель задачи
    """
    title: str
    description: str


class TaskDetailsModel(TaskModel):
    """
    Детальная модель задачи
    """
    id: int
    user_name: str
