from rest_framework.authtoken.models import Token

from main.models import User


def token_from_user(user_id: int):
    token, created = Token.objects.get_or_create(user_id=user_id)
    return token
