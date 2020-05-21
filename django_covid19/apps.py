from django.apps import AppConfig


class DjangoCovid19Config(AppConfig):
    name = 'django_covid19'
    verbose_name = '新冠肺炎疫情'

    def ready(self):
        import django_covid19.signals