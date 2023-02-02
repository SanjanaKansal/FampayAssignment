import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'custom_youtube.settings')

app = Celery('custom_youtube')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'youtube.tasks.get_latest_videos_from_youtube',
        'schedule': 10.0,
    }
}
