from django.dispatch import receiver
from django.core.cache import cache
from django.core.signals import request_finished
 
@receiver(request_finished)
def my_callback(sender, **kwargs):
    if cache.get('crawled'):
        cache.clear()