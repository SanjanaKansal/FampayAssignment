from django.db import models

# Create your models here.


class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=256, null=False, unique=True)
    title = models.CharField(max_length=256, null=False, db_index=True)
    description = models.TextField(default='', db_index=True)
    thumbnail_url = models.URLField()
    published_datetime = models.DateTimeField(db_index=True)
