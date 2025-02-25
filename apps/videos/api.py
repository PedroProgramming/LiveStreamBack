import json
from typing import Tuple
from users.models import User
from core.auth import JWTAuth
from ninja import File, Router, Form
from channel.models import Channel
from django.http import HttpRequest
from ninja.files import UploadedFile

from .models import Video
from .tasks import process_video
from .schemas import CreateVideoSchema, VideoSchema, VideoResponseSchema

video_router = Router(
    auth=JWTAuth()
)

#TODO ERRO AO INSERIR VÍDEO
@video_router.post("/upload", response={201: dict, 400: dict, 404: dict, 500: dict})
def upload_video(request: HttpRequest, video_data: CreateVideoSchema, video_file: UploadedFile = File(...)) -> Tuple[int, dict]:
    print(video_file)
    try:
        user = User.objects.get(id=request.user)
    except user.DoesNotExist:
        return 404, {"error": "User not does exist"}
    try:
        channel = Channel.objects.get(user=user)
    except user.DoesNotExist:
        return 404, {"error": "Channel not does exist"}

    try:
        video = Video(
            channel=channel,
            title=video_data.title,
            description=video_data.description,
        )
        video.save()

        video_bytes = video_file.read()
        process_video.delay(video.id, video_bytes)

        return 201, {"success": "Video created successfully"}
    except (ValueError, NameError) as e:
        print(str(e))
        return 400, {"error": f"{str(e)}"}
    
    except Exception as e:
        return 500, {"error": f"{str(e)}"}

@video_router.get("/list", response={200: VideoResponseSchema}, auth=None)
def all_videos(request: HttpRequest) -> Tuple[int, dict]:
    videos = [
        VideoSchema(
            id=video.id,
            identifier=video.identifier,
            title=video.title,
            description=video.description,
            thumbnail_url=video.thumbnail.url if video.thumbnail else "",
            views=video.views,
            likes=video.likes,
            dislikes=video.dislikes,
            video_url=video.get_video_url("1080p")
        ) for video in Video.objects.all()
    ]
    return 200, {"videos": videos}

@video_router.get("/{channel_name}", response={200: VideoResponseSchema, 404: dict})
def list_videos_channel(request: HttpRequest, channel_name: str) -> Tuple[int, dict]:
    try:
        channel = Channel.objects.get(channel_name__exact=channel_name)
    except channel.DoesNotExist:
        return 404, {"Channel does not exist"}
    
    videos_channel = Video.objects.filter(channel=channel)

    videos = [
        VideoSchema(
            id=video.id,
            identifier=video.identifier,
            title=video.title,
            description=video.description,
            thumbnail_url=video.thumbnail.url if video.thumbnail else "",
            views=video.views,
            likes=video.likes,
            dislikes=video.dislikes,
            video_url=video.get_video_url("1080p")
        ) for video in videos_channel
    ]
    return 200, {"videos": videos}

@video_router.get("/detail/{identifier}", response={200: VideoSchema, 404: dict})
def get_video(request: HttpRequest, identifier: str) -> Tuple[int, dict]:
    try:
        video = Video.objects.get(identifier__exact=identifier)
    except video.DoesNotExist:
        return 404, {"Video does not exist"}
    
    video_detail = VideoSchema(
        id=video.id,
        identifier=video.identifier,
        title=video.title,
        description=video.description,
        thumbnail_url=video.thumbnail.url if video.thumbnail else "",
        views=video.views,
        likes=video.likes,
        dislikes=video.dislikes,
        video_url=video.get_video_url("1080p")
    )
    return 200, video_detail.dict()