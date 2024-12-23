import os
import ffmpeg
from django.conf import settings

class LiveStreamProcessor:
    def __init__(self, stream_key, segment_file, segment_bytes):
        self.stream_key = stream_key
        self.segment_file = segment_file
        self.segment_bytes = segment_bytes
        self.output_dir = os.path.join(settings.MEDIA_ROOT, "livestreams", stream_key, "processed")
        os.makedirs(self.output_dir, exist_ok=True)

    def _process_resolutions(self):
        resolutions = {
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

        resolution_files = {}

        for res, size in resolutions.items():
            resolution_dir = os.path.join(self.output_dir, res)
            os.makedirs(resolution_dir, exist_ok=True)
            output_file = os.path.join(resolution_dir, f"{self.segment_file}_{res}.ts")

            ffmpeg.input("pipe:0").output(
                output_file,
                vf=f"scale={size['width']}:{size['height']}",
                vcodec="libx264",
                acodec="aac",
                f="mpegts"
            ).run(input=self.segment_bytes)

            resolution_files[res] = output_file

        return resolution_files

    def process(self):
        return self._process_resolutions()
