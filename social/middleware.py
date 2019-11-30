import logging

from django.utils.cache import add_never_cache_headers

logger = logging.getLogger(__name__)

"""
https://stackoverflow.com/questions/49547/how-do-we-control-web-page-caching-across-all-browsers/2068407#2068407

https://stackoverflow.com/questions/2095520/fighting-client-side-caching-in-django
"""


class DisableClientCachingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        logger.debug('__init__')

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        logger.debug('__call__')
        return response
