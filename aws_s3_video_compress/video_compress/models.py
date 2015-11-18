from django.db import models
from datetime import datetime


class Video(models.Model):
    video = models.FileField(upload_to='zaya-videos')
    title = models.CharField(max_length=200, unique=True)
    time = models.DateTimeField()
    compressed_video = models.FileField(upload_to='zaya-videos', blank=True)

    def save(self, *args, **kwargs):
        self.time = datetime.now()
        super(Video, self).save(*args, **kwargs)
