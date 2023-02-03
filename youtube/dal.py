from datetime import datetime

import pytz
from django.db.models import Q

from youtube import models


def save_videos(videos_data):
    """Saves videos in DB."""
    if not videos_data['items']:
        return
    youtube_videos_list = []
    for item in videos_data['items']:
        snippet = item['snippet']
        thumbnails = snippet['thumbnails']
        youtube_videos_list.append(
            models.YoutubeVideo(
                video_id=item['id']['videoId'],
                title=snippet['title'],
                description=snippet['description'],
                thumbnail_url=thumbnails['default']['url'],
                published_datetime=snippet['publishedAt'],
            )
        )
    models.YoutubeVideo.objects.bulk_create(youtube_videos_list, ignore_conflicts=True)


def get_videos_and_sync_token(search_query: str, sync_token: int, limit: int = 10):
    """Returns latest videos from DB and the sync_token to get next set of videos."""
    if not sync_token:
        all_videos = models.YoutubeVideo.objects.order_by('-published_datetime')
    else:
        sync_datetime = datetime.utcfromtimestamp(sync_token).replace(tzinfo=pytz.UTC)
        all_videos = models.YoutubeVideo.objects.filter(
            published_datetime__lt=sync_datetime
        ).order_by('-published_datetime')

    if search_query:
        all_videos = all_videos.filter(
            Q(title=search_query)
            | Q(description=search_query)
            | Q(title__contains=search_query)
            | Q(description__contains=search_query)
        )

    videos = list(
        all_videos.values(
            'video_id', 'title', 'description', 'thumbnail_url', 'published_datetime'
        )[:limit]
    )

    if not videos:
        return None, None

    # Extend Videos limit till sync_token from the next element is not same.
    if all_videos.count() > limit:
        for i in range(min(all_videos.count(), limit)):
            if videos[-1]['published_datetime'].strftime('%s') != all_videos[
                limit + i
            ].published_datetime.strftime('%s'):
                break
            videos.append(all_videos[limit + i].__dict__)

    new_sync_token = videos[-1]['published_datetime'].strftime('%s')
    return videos, new_sync_token
