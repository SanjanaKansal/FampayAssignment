import datetime
import os

import pytz
from pyrfc3339 import generate

from youtube import constants


def get_headers():
    return {'Content-Type': 'application/json'}


def _get_published_before():
    # There is no information in the youtube API documentation regarding the publishedAt field
    # whether it is the time when video upload started or video upload finished or video
    # metadata inserted in DB from where query is done. So, the method is fetching 10 minutes older
    # videos assuming video upload doesn't take more than 10 minutes on average.
    return generate(datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(minutes=10))


def _get_published_after():
    return generate(
        datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        - datetime.timedelta(minutes=10, seconds=10)
    )


def get_params(
    key: str = os.environ['YOUTUBE_API_KEY'],
    type: str = 'video',
    order: str = 'date',
    search_query: str = constants.PREDEFINED_SEARCH_QUERY,
    part: str = 'snippet',
):
    """Returns params for Youtube Search API."""
    return {
            constants.AUTH_KEY: key,
            constants.TYPE_KEY: type,
            constants.ORDER_KEY: order,
            constants.PUBLISHED_BEFORE_KEY: _get_published_before(),
            constants.PUBLISHED_AFTER_KEY: _get_published_after(),
            constants.SEARCH_KEY: search_query,
            constants.PART_KEY: part
        }
