# streaming/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='tracks/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)  # <== добавлено поле

    def __str__(self):
        return f"{self.title} - {self.artist}"

class ListeningSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    listened_seconds = models.IntegerField(default=0)
    rewarded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} listened to {self.track}"
