import requests
from celery import task

from youtube import constants, dal, private


@task
def get_latest_videos_from_youtube():
    """Returns Youtube latest data related to query 'football' limited to 5 results by default.

    Pass the params in private._get_params method for customised results.

    Reference:
            https://developers.google.com/youtube/v3/docs/search/list

    """
    response = requests.get(
        constants.BASE_URL + 'search',
        headers=private.get_headers(),
        params=private.get_params(),
    )
    if response.status_code != requests.codes.ok:
        return
    dal.save_videos(response.json())
