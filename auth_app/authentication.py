from rest_framework.authentication import TokenAuthentication


class MyTokenAuthentication(TokenAuthentication):
    keyword = 'token_auth'