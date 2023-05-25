"""
Подключаем базу данных
"""
import databases


DB_USER = 'admin'
DB_PASSWORD = 'Qq123456'
DB_HOST = 'localhost'
DB_NAME = "gooddelott2"

database = databases.Database(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}')
