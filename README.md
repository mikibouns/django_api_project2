# django_api_project

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

2) `python manage.py fill_db` - очищает БД и заполняет ее тестовыми данными которые хранятся в [data_for_testing.json](https://github.com/mikibouns/django_api_project2/blob/master/data_for_testing.json) в формате JSON

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
#### Документация API нахоиться в [этом](https://github.com/mikibouns/django_api_project2/blob/dev_2.1/api_app/templates/api_app/api_docs.html) файле и доступна из веб приложения http://127.0.0.1:8000/api-doc/
