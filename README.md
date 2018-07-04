# django_api_project
[Аутентификация](https://github.com/mikibouns/django_api_project2/blob/master/README.md#%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F)



[install_manual.txt](https://github.com/mikibouns/django_api_project2/blob/master/install_manual.txt) поможет вам установить и настроить приложение для работы

После [установки и настройки](https://github.com/mikibouns/django_api_project2/blob/master/install_manual.txt) проекта вам будет доступна панель администрирования по адресу http://127.0.0.1:8000/admin/.
Учетные данные суперпользователя следующие: 
```
login: admin
password: admins_password
```

### Аутентификация:

- Basic Auth

Стандартная аутентификация использующая логин и пароль:
```
curl -u admin:admins_password http://127.0.0.1:8000/v1/
```

- Token Auth

Чтобы получить токен пользователя необходимо совершить `POST` запрос по адресу `http://127.0.0.1:8000/v1/api-token-auth/` передав в теле запроса `{"username": "<username>", "password": "<password>"}` в формате JSON, в ответ вы получите `{"token": "<token>"}` 

Для аутентификации в header http запроса передается  "Authorization: token_auth `<token>`":
```
curl -X GET http://127.0.0.1:8000/v1/ -H "Authorization: token_auth <token>"
```
