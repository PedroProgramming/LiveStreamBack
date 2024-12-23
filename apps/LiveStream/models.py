from django.db import models

class LiveStream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="Estou ao vivo")

    stream_key = models.CharField(max_length=255, unique=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    resolutions = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.stream_key:
            self.stream_key = self._generate_stream_key()
        super(LiveStream, self).save(*args, **kwargs)

    def _generate_stream_key(self):
        import uuid
        return uuid.uuid4().hex

    def __str__(self):
        return f"{self.title} | {self.stream_key}"