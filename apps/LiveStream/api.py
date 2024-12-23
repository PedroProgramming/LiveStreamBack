import threading

from typing import Tuple
from ninja import Router
from django.http import HttpRequest
from ninja.files import UploadedFile
from scripts.monitor_hls import monitor_hls_directory

from .models import LiveStream
from .tasks import process_live_segment


stream_router = Router()

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
        print(str(e))
        return 400, {"code": 1}
    
    live.is_active = True
    live.save()

    thread = threading.Thread(target=monitor_hls_directory, args=(data["name"],))
    thread.start()
    return 200, {"code": 0}
    
@stream_router.post("/end", response={200: dict, 400: dict})
def end_live(request: HttpRequest):
    data = request.POST

    try:
        live = LiveStream.objects.get(stream_key__exact=data["name"], is_active=True)
    except LiveStream.DoesNotExist:
        return 400, {"code": 1}

    live.is_active = False
    live.save()
    return 200, {"code": 0}

@stream_router.post("/upload_segment/{stream_key}", response={200: dict, 400: dict})
def upload_segment(request: HttpRequest, file: UploadedFile, stream_key: str):
    print(stream_key)
    try:
        live = LiveStream.objects.get(stream_key__exact=stream_key)
        
    except LiveStream.DoesNotExist:
        return 400, {"status": "error", "message": "Invalid stream key"}

    segment_bytes = file.read()
    process_live_segment.delay(live.stream_key, file.name, segment_bytes)
    return 200, {"status": "success"}