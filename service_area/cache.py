from django.core.cache import cache
from django.conf import settings


class CacheService:

    @staticmethod
    def set(name, value, expire=settings.MAX_CACHE_EXPIRE_TIME):
        try:
            cache.set(name, value, timeout=expire)
        except Exception as e:
            raise CacheError('error setting cache') from e

    @staticmethod
    def get(name, default=None):
        if not default:
            default = {}
        try:
            data = cache.get(name, default)
        except Exception as e:
            raise CacheError('an error getting from cache') from e
        return data

    @staticmethod
    def delete(name):
        try:
            cache.delete(name)
        except Exception as e:
            raise CacheError('an error deleting cache') from e

class CacheError(Exception):
    pass
