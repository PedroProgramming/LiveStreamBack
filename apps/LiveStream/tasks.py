import uuid
from celery import shared_task

from .live_processor import monitor_hls_directory


@shared_task
def process_live_segment(stream_key: uuid) -> str:
    monitor_hls_directory(stream_key)
    return "Transmission ended"