import datetime

from django.conf import settings
from django.core.cache import get_cache

from doctor.services import BaseServiceCheck


class CacheServiceCheck(BaseServiceCheck):
    """
    Check the status of the cache backends.
    """

    name = 'Cache'
    #template = ''

    def status(self):

        caches_info = {}

        # Cache check
        for cache_name in settings.CACHES.keys():

            is_cache_working = True

            # Try to get the cache backend
            try:
                cache = get_cache(cache_name)
            except Exception as ex:
                is_cache_working = False
                cache_message = str(ex)

            # Check the cache backend
            if is_cache_working:
                CACHE_KEY = 'doctor-cache-check-%s' % cache_name
                cache_message = cache.get(CACHE_KEY, None)

                # If cache is empty, update cache
                if cache_message is None:

                    # Set timestamped message in cache
                    cache_message = 'From cache, set at %s' % datetime.datetime.now()
                    cache.set(CACHE_KEY, cache_message, 10)

                    if cache_message != cache.get(CACHE_KEY):
                        is_cache_working = False

                    # Get again, to see if the message is persisted in cache
                    cache_message = cache.get(CACHE_KEY, 'Data not persisted in cache.')

            # Create dictionary with status info
            caches_info[cache_name] = {
                'is_working': is_cache_working,
                'message': cache_message,
                'settings': settings.CACHES[cache_name],
            }
        return caches_info
