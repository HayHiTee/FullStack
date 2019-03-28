from django.apps import AppConfig


class FullstackappConfig(AppConfig):
    name = 'FullStackApp'


    def ready(self):
        import FullStackApp.hooks
