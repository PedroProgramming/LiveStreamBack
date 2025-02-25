from typing import Tuple
from ninja import Router
from django.http import HttpRequest
from ninja.files import UploadedFile

from .models import LiveStream
from .tasks import process_live_segment
from .schemas import LiveStreamSchema, LiveResponseSchema

stream_router = Router()

@stream_router.get("/list", response={200: LiveResponseSchema}, auth=None)
def list_stream(request: HttpRequest):
    lives = [
        LiveStreamSchema(
            id=live.id,
            stream_key=live.stream_key,
            title=live.title,
            description=live.description,
        ) for live in LiveStream.objects.filter(is_active=True)
    ]
    return 200, {"lives": lives}

@stream_router.post("/create")
def create_live(request: HttpRequest, title: str):
    live = LiveStream(title=title)
    live.save()
    return {"id": live.id, "title": live.title, "stream_key": live.stream_key}

@stream_router.post("/validate_stream_key", response={200: dict, 400: dict})
def validate_stream_key(request: HttpRequest) -> Tuple[int, dict]:
    data = request.POST

    try:
        live = LiveStream.objects.get(stream_key__exact=data["name"], is_active=False)
    except LiveStream.DoesNotExist as e:
        return 400, {"code": 1}
    
    live.is_active = True
    live.save()

    process_live_segment.delay(live.stream_key)
    return 200, {"code": 0}
    
@stream_router.post("/end", response={200: dict, 400: dict})
def end_live(request: HttpRequest):
    data = request.POST

    try:
        live = LiveStream.objects.get(stream_key__exact=data["name"], is_active=True)
    except LiveStream.DoesNotExist:
        return 400, {"code": 1}
    
    live.is_active = not live.is_active
    live.save()
    return 200, {"code": 0}

@stream_router.post("/upload_segment/{stream_key}", response={200: dict, 400: dict})
def upload_segment(request: HttpRequest, file: UploadedFile, stream_key: str):
    try:
        live = LiveStream.objects.get(stream_key__exact=stream_key)
    except LiveStream.DoesNotExist:
        return 400, {"status": "error", "message": "Invalid stream key"}

    segment_bytes = file.read()
    process_live_segment.delay(live.stream_key, file.name, segment_bytes)
    return 200, {"status": "success"}