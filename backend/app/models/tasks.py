"""
Таблица для задач
"""
import sqlalchemy

from .users import users_table


metadata = sqlalchemy.MetaData()

tasks_table = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column("title", sqlalchemy.String(250)),
    sqlalchemy.Column("description", sqlalchemy.Text()),
)
