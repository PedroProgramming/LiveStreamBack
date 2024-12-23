import jwt
from users.models import User
from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import TokenError


class InvalidToken(Exception):
    ...


class JWTAuth(HttpBearer):
    """
        Custom JWT Authentication class for Ninja API.
    """
     
    def authenticate(self, request: HttpRequest, token: str):
        try:
            data = jwt.decode(
                token, settings.SIGNING_KEY, algorithms=settings.ALGORITHM
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise InvalidToken("The token has expired.")
        except jwt.exceptions.InvalidTokenError:
            raise InvalidToken("The token is invalid.")

        user = User.objects.filter(id=data['user_id']).first()
        if user:
            request.user = user.id
            return user.id

        raise InvalidToken('Invalid Token')
