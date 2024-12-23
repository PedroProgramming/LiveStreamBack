from ninja import Router
from typing import Tuple
from core.auth import JWTAuth
from users.models import User
from django.http import HttpRequest
from videos.api import video_router


from .models import Channel
from .schemas import CreateChannelSchema, DetailsChannelSchema


channel_router = Router(
    auth=JWTAuth()
)

channel_router.add_router("/videos", video_router)

@channel_router.post("/create", response={201: dict, 400: dict, 404: dict, 409: dict, 500: dict})
def create_channel(request: HttpRequest, channel_data: CreateChannelSchema) -> Tuple[int, dict]:
    
    try:
        user = User.objects.get(id=request.user)
    except user.DoesNotExist:
        return 404, {"error": "User not does exist"}
    
    if Channel.objects.filter(user=user).exists():
        return 409, {"error": "This user already has a registered channel"}

    try:
        channel = Channel(
            user=user,
            channel_name=channel_data.channel_name,
            description=channel_data.description
        )
        channel.save()
        
        return 201, {"success": "Channel created successfully"}
    except (ValueError, NameError) as e:
        return 400, {"error": f"{str(e)}"}
    
    except Exception as e:
        return 500, {"error": f"{str(e)}"}

# TODO Criar rota para atualizar informações do canal

@channel_router.get("/details/{channel_name}", response={200: DetailsChannelSchema, 404: dict})
def details_channel(request: HttpRequest, channel_name: str) -> Tuple[int, dict]:
    try:
        channel = Channel.objects.get(channel_name__exact=channel_name)
    except channel.DoesNotExist:
        return 404, {"error:": "Channel not found"}
    
    details_channel = DetailsChannelSchema(channel_name=channel.channel_name, description=channel.description, subscribers_count=channel.subscribers_count)
    return 200, details_channel.dict()

@channel_router.get("/verify", response={200: dict, 404: dict})
def verify_channel(request: HttpRequest) -> Tuple[int, dict]:
    try:
        channel = Channel.objects.get(user=User.objects.get(id=request.user))
        return 200, {"channel_name": channel.channel_name}
    except Exception as e:
        print(str(e))
        return 404, {"error:": f"{str(e)}"}