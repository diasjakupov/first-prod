from django.apps import AppConfig


class WallConfig(AppConfig):
    name = 'wall'

    def ready(self):#import django-signals
        import wall.signals