from ninja import File
from ninja import Router
from core.auth import JWTAuth
from typing import Tuple, Optional
from django.http import HttpRequest
from ninja.files import UploadedFile
from django_ratelimit.decorators import ratelimit
from django.core.exceptions import ObjectDoesNotExist
from utils.verification import check_rate_limit_status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .schemas import DetailsUserSchema, UpdateUserSchema

user_router = Router(
    auth=JWTAuth()
)

@ratelimit(key="ip", rate="50/h", block=False)
@user_router.get("/details", response={200: DetailsUserSchema, 400: dict, 404: dict, 429: dict, 500: dict})
def user_datails(request: HttpRequest) -> Tuple[int, dict]:
    status_code, response_data = check_rate_limit_status(request, limit=50)
    if status_code != 200:
        return status_code, response_data
    
    user = User.objects.get(id=request.user)

    try:
        user_details = DetailsUserSchema(username=user.username, email=user.email, profile_picture_url=user.profile_picture.url)
        return 200, user_details.dict()
    except User.DoesNotExist:
        return 404, {"error": "User not found"}
    
    except Exception as e:
        print(f"{str(e)}")
        return 500, {"error": "An unexpected error occurred", "details": str(e)}

@ratelimit(key="ip", rate="10/h", block=False)
@user_router.patch("/update", response={200: dict, 400: dict, 404: dict, 429: dict, 500: dict})
def update_details(request: HttpRequest, user_update: Optional[UpdateUserSchema] = None) -> Tuple[int, dict]:
    # TODO Receber e atualizar imagem. Na mesma rota das informações ou não?

    status_code, response_data = check_rate_limit_status(request, limit=10)
    if status_code != 200:
        return status_code, response_data
    
    try:
        user = User.objects.get(id=request.user)

        if user_update:
            for attr, value in user_update:
                if value is not None:
                    setattr(user, attr, value)
        user.save()

        return 200, {"message": "User updated successfully", "user": {"username": user.username, "email": user.email}}

    except ObjectDoesNotExist:
        return 404, {"error": "User not found"}

    except Exception as e:
        return 500, {"error": "An unexpected error occurred", "details": str(e)}

@ratelimit(key="ip", rate="10/h", block=False)
@user_router.post("/profile-picture", response={200: dict, 404: dict, 429: dict, 500: dict})
def upload_profile_picture(request: HttpRequest, profile_picture: UploadedFile = File(...)) -> Tuple[int, dict]:

    status_code, response_data = check_rate_limit_status(request, limit=10)
    if status_code != 200:
        return status_code, response_data
    
    try:
        user = User.objects.get(id=request.user)
        user.profile_picture.save(profile_picture.name, profile_picture, save=True)
        user.save()

        return 200, {"message": "Profile picture updated successfully", "profile_picture": user.profile_picture.url}
    except ObjectDoesNotExist:
        return 404, {"error": "User not found"}
    except Exception as e:
        return 500, {"error": "Failed to update profile picture", "details": str(e)}

@user_router.post("/refresh-token", response={200: dict, 400: dict, 500: dict})
def refresh_user_token(request: HttpRequest, refresh_token: str) -> Tuple[int, dict]:
    user = User.objects.get(id=request.user)

    try:
        refresh_old_token = RefreshToken(refresh_token)
        refresh_old_token.blacklist()
        
        refresh_token_new = RefreshToken.for_user(user)
        access_token = str(refresh_token_new.access_token)

        return 200, {"access_token": str(access_token),"refresh_token": str(refresh_token_new)}
    
    except Exception as e:
        return 500, {"error": "An unexpected error occurred", "details": str(e)}