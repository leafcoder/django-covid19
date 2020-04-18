from django.apps import AppConfig


class NcovapiConfig(AppConfig):
    name = 'ncovapi'
    verbose_name = '新冠肺炎疫情'

    def ready(self):
        import ncovapi.signals