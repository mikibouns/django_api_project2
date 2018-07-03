# django_api_project
install_manual.txt. вам поможет установить и настроить приложение для работы

Аутентификация:
1)	Basic Auth
Стандартная аутентификация использующая логин и пароль:

curl -u admin:admins_password http://127.0.0.1:8000/v1/

2)	Token Auth
В header запроса передается  “Authorization: token_auth <token>” для аутентификации:

curl -X GET http://127.0.0.1:8000/v1/ -H "Authorization: token_auth 34295a6efee00d4c775b8274619aa0ec7691fac6"
