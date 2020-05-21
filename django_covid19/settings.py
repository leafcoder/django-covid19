from django.conf import settings

CACHE_PAGE_TIMEOUT = getattr(settings, 'CACHE_PAGE_TIMEOUT', 24*60*60)