import os, string, random

from django.db import models
from django.conf import settings
from django.utils import timezone
from channel.models import Channel


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")

    identifier = models.CharField(max_length=10, unique=True, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="Este vídeo não possui uma descrição")
    upload_date = models.DateTimeField(auto_now_add=True)

    thumbnail = models.ImageField(upload_to="videos/thumbnails/", blank=True, null=True)

    resolutions = models.JSONField(default=dict)
    is_processed = models.BooleanField(default=False)
    processing_date = models.DateTimeField(blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-upload_date"]
        verbose_name = "Vídeo"
        verbose_name_plural = "Vídeos"

    def __str__(self):
        return f"{self.title} ({self.identifier})"

    @staticmethod
    def generate_unique_identifier() -> str:
        while True:
            identifier = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            if not Video.objects.filter(identifier=identifier).exists():
                return identifier
            
    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_unique_identifier()
        super().save(*args, **kwargs)

    def get_video_url(self, resolution):
        return os.path.join(settings.MEDIA_URL, "videos", "processed", self.identifier, resolution, f"{self.identifier}_{resolution}.mp4")

    def process_video(self):
        self.is_processed = True
        self.processing_date = timezone.now()