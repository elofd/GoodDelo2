# GoodDeloTT2  
В основу проекта лёг фреймворк FastAPI   
Чтобы установить, нужно склонировать репозиторий и установить пакеты из requirements.txt  
Функциональность, которая реализована:  

* Регистрация нового пользователя (POST-запрос на /register)
* Авторизация пользователя (POST-запрос на /login)
* Разлогинивание пользователя (POST-запрос на /logout)
* Создание новой записи (POST-запрос на /tasks)
* Получение списка всех записей (GET-запрос на /tasks)
* Получение конкретной записи (GET-запрос на /tasks/{task_id})
* Изменение записи (PUT-запрос на /tasks/{task_id})
* Удаление записи (DELETE-запрос на /tasks/{task_id})
