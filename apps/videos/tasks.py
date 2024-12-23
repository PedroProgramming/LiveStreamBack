import tempfile

from celery import shared_task

from .models import Video
from .video_processor import VideoProcessor

@shared_task
def process_video(video_id: int, video_bytes: bytes) -> str:
    try:
        video = Video.objects.get(id=video_id)

        process = VideoProcessor(video, video_bytes)
        resolutions = process.process()

        video.resolutions = resolutions

        video.process_video()
        video.save()

    except Video.DoesNotExist:
        return f"Video with ID {video_id} not found."
    except Exception as e:
        return str(e)