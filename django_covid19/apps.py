from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoCovid19Config(AppConfig):
    name = 'django_covid19'
    verbose_name = _('django_covid19')

    def ready(self):
        import django_covid19.signals