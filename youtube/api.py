from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from youtube import dal


class YoutubeResource(Resource):
    class Meta:
        resource_name = 'youtube'
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/videos%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_videos'),
                name="api_get_videos",
            ),
        ]

    def get_videos(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        sync_token = int(request.GET.get('sync_token', 0))
        videos, sync_token = dal.get_videos_and_sync_token(search_query, sync_token)
        return self.create_response(
            request, {'videos': videos, 'sync_token': sync_token}
        )
