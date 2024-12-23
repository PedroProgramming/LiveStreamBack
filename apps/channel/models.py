from django.db import models
from users.models import User

class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="channels")
    channel_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, default="Este canal não adicionou nenhuma descrição")
    profile_image = models.ImageField(upload_to='channel/profile_images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='channel/banner_images/', blank=True, null=True)
    subscribers_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.channel_name

    def increment_subscribers(self):
        self.subscribers_count += 1
        self.save()

    def decrement_subscribers(self):
        if self.subscribers_count > 0:
            self.subscribers_count -= 1
            self.save()
