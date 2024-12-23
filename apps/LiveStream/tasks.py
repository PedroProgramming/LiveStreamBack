import uuid
from celery import shared_task

from .models import LiveStream
from .live_processor import LiveStreamProcessor

@shared_task
def process_live_segment(stream_key: uuid, file_name: str, segment_bytes: bytes) -> str:
    try:
        live = LiveStream.objects.get(stream_key=stream_key)

        process = LiveStreamProcessor(stream_key, file_name, segment_bytes)
        resolutions = process.process()

        live.resolutions = resolutions
        live.save()

    except LiveStream.DoesNotExist:
        return f"Live with StreamKey {stream_key} not found."
    except Exception as e:
        return str(e)