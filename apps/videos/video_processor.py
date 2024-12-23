import os
import ffmpeg
from django.conf import settings

class VideoProcessor:
    def __init__(self, video, video_bytes):
        self.video = video
        self.video_bytes = video_bytes
        self.output_dir = os.path.join(settings.MEDIA_ROOT, "videos", "processed", video.identifier)
        os.makedirs(self.output_dir, exist_ok=True)

    def _process_resolutions(self):
        resolutions = {
            "240p": {
                "width": 426,
                "height": 240
            },
            "360p": {
                "width": 640,
                "height": 360
            },
            "480p": {
                "width": 854,
                "height": 480
            },
            "720p": {
                "width": 1280,
                "height": 720
            },
            "1080p": {
                "width": 1920,
                "height": 1080
            },
        }
        resolutions_files = {}

        for res, size in resolutions.items():
            resolution_dir = os.path.join(self.output_dir, res)
            os.makedirs(resolution_dir, exist_ok=True)
            output_file = os.path.join(resolution_dir, f"{self.video.identifier}_{res}.mp4")
            ffmpeg.input("pipe:0").output(
                output_file,
                vf=f"scale={size["width"]}:{size["height"]}",
                vcodec="libx264",
                acodec="aac"
            ).run(input=self.video_bytes)

            resolutions_files[res] = output_file

        return resolutions_files
    
    def process(self):
        resolutions = self._process_resolutions()
        return resolutions
