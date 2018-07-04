# django_api_project
[Установка и настройка](#Установка-и-настройка)  
[Аутентификация](#Аутентификация)

## Установка и настройка:

Установить python версией не ниже 3.4 ==> https://www.python.org/downloads/ далее, запустить файл установки виртуальной среды [install_env.py](https://github.com/mikibouns/django_api_project2/blob/master/install_env.py), для этого необходимо находиться в каталоге проекта (django_api_project2):
  + *Windows*  
     ```python install_env.py```
  + *Linux*  
     ```python3 install_env.py```   
     или  
     ```chmod +x install_env.py && ./install_env.py```  
  + *MacOS*  
     ```python3 install_env.py```  

### Активация виртуальной среды
Активировать виртуальную можно следующим способом, для этого необходимо находиться в каталоге проекта (django_api_project2):  
  + *Windows*  
      ```venv\Scripts\activate.bat```
      > возможно прийдется указать абсолютный путь в файлу `activate.bat`
  + *Linux*  
      ```. env/bin/activate```  
      или  
      ```source env/bin/activate```  
  + *MacOS*  
     ```. env/bin/activate```  
     или  
     ```source env/bin/activate```
     > Деактивируется виртуальная среда командой `deactivate`

### Команды выполняемые в виртуальной среде

> Данные команды следует выполнить в порядке очереди для настройки базы данных

1) `python manage.py update_db` - удаляет созданные миграции и БД, затем
   создает заново

2) `python manage.py fill_db` - очищает БД и заполняет ее тестовыми данными которые хранятся в [data_for_testing.py](https://github.com/mikibouns/django_api_project2/blob/master/data_for_testing.py) в формате JSON

> Команда для запуска сервера

1) `python manage.py runserver` - запускает локальный веб-сервер,
   который доступен по адресу 127.0.0.1:8000.
   Если нужно указать другой порт или сделать
   адрес доступным в локальной сети то выполняем следующую команду:
   python manage.py runserver 0.0.0.0:8080 - где 8080 это номер порта

После [установки и настройки](#Установка-и-настройка) проекта вам будет доступна панель администрирования по адресу http://127.0.0.1:8000/admin/.
Учетные данные суперпользователя следующие: 
```
login: admin
password: admins_password
```

## Аутентификация:
API поддерживает 2-а вида аутентификации:
- Basic Auth  
  - Стандартная аутентификация использующая логин и пароль:  
```curl -u admin:admins_password http://127.0.0.1:8000/v1/```

- Token Auth  
  - Чтобы получить токен пользователя необходимо совершить `POST` запрос по адресу `http://127.0.0.1:8000/v1/api-token-auth/`   передав в теле запроса `{"username": "<username>", "password": "<password>"}` в формате JSON, в ответ вы получите `{"token": "<token>"}` 

  - Для аутентификации в header http запроса передается  "Authorization: token_auth `<token>`":  
```curl -X GET http://127.0.0.1:8000/v1/ -H "Authorization: token_auth <token>"```
    > Срок жизни токена 30 дней
    
## Соглашение:
Согласно данному соглашению будет определен формат и протокол обмена данными
### Ошибки
Формат: **JSON**  
Параметры:
  - `message` - содержит номер HTTP ошибки (400, 403, 404, ...)
  - `success` - сожердит 0 (в случае успеха 1)
  - `exception` - содержит описание ошибки
Пример:
```
{
    "message": 403,
    "success": 0,
    "exception": "Authentication credentials were not provided."
}
```
