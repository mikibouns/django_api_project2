# django_api_project
install_manual.txt. поможет вам установить и настроить приложение для работы

### Аутентификация:


- Basic Auth

Стандартная аутентификация использующая логин и пароль:
`curl -u admin:admins_password http://127.0.0.1:8000/v1/`

- Token Auth

Чтобы получить токен пользователя необходимо совершить `POST` запрос по адресу `http://127.0.0.1:8000/v1/api-token-auth/` передав в теле запроса `{"username": "<username>", "password": "<password>"}` в формате JSON, в ответ вы получите `{"token": "<token>"}` 

Для аутентификации в header http запроса передается  "Authorization: token_auth `<token>`":
`curl -X GET http://127.0.0.1:8000/v1/ -H "Authorization: token_auth 34295a6efee00d4c775b8274619aa0ec7691fac6"`
