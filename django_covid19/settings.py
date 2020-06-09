from django.conf import settings

CACHE_PAGE_TIMEOUT = getattr(settings, 'CACHE_PAGE_TIMEOUT', 24*60*60)

SCRAPY_LOG_FILE = getattr(settings, 'SCRAPY_LOG_FILE', None)