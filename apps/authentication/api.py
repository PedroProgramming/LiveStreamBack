from ninja import Router
from typing import Tuple
from users.models import User
from core.auth import JWTAuth
from django.http import HttpRequest
from django.db import IntegrityError
from users.backends import CustomBackend
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from utils.validations import validate_password
from utils.verification import check_rate_limit_status

from .schemas import UserCreateSchema, LoginSchema

auth_router = Router()

@ratelimit(key="ip", rate="20/h", block=False)
@auth_router.post('/register', response={201: dict, 400: dict, 429: dict, 500: dict})
def register(
    request: HttpRequest, user_register: UserCreateSchema
) -> Tuple[int, dict]:
    """
        - User.objects.filter(email__exact=user_data.email).exists()
        If users exists Return Error with status 400 Otherwise continue

        - if not validate_password
        If password and password confirmation are not the same or password is incorrect Return Error with status 400 Otherwise continue
    
        - User.objects.create_user
        If the data is correct Returns Success with status 201
        Create a new user and save to the database
        Otherwise Error
    """

    status_code, response_data = check_rate_limit_status(request, limit=20)
    if status_code != 200:
        return status_code, response_data
    
    if User.objects.filter(email__exact=user_register.email).exists():
        return 400, {'error': 'Username already exists'}

    if not validate_password(user_register.password, user_register.confirm_password):
        return 400, {'error': 'Passwords are unknown or incorrect'}

    try:
        user = User.objects.create_user(
            username=user_register.username,
            email=user_register.email,
            password=user_register.password,
        )

        return 201, {'message': 'User registered successfully!'}

    except IntegrityError:
        return 400, {'error': 'Username or email already exists'}

    except Exception as e:
        return 500, {"error": "An unexpected error occurred", "details": str(e)}

@ratelimit(key="ip", rate="20/h", block=False)
@auth_router.post('/login', response={200: dict, 400: dict, 429: dict})
def login(request: HttpRequest, user_login: LoginSchema) -> Tuple[int, dict]:

    """
        - CustomBackend().authenticate()
        If users exists Return Error with status 400

        If user exists, creates Access Token and Access Token
        Refresh Token and returns Success and status 200

    """
    status_code, response_data = check_rate_limit_status(request, limit=20)
    if status_code != 200:
        return status_code, response_data

    user = CustomBackend().authenticate(
        request, user_login.email, user_login.password
    )

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return 200, {
            'message': 'Login successfull',
            'access_token': str(access),
            'refresh_token': str(refresh),
        }
    return 400, {'error': 'Invalid credentials or user does not exist.'}

@auth_router.post("/logout", response={200: dict, 400: dict, 500: dict}, auth=JWTAuth())
def logout(request: HttpRequest, refresh_token: str) -> Tuple[int, dict]:
    """
        - Invalidates the refresh token sent by the client.
        - Blacklist: Marks the token as invalid and prevents further use.
    """

    if not refresh_token:
        return 400, {"error": "Refresh token is required"}

    try:
        token = RefreshToken(refresh_token)
    except Exception as e:
        return 500, {"error": "An unexpected error occurred", "details": str(e)}
    
    token.blacklist()
    return 200, {"message": "Logout successful"}
