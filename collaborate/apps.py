from django.apps import AppConfig


class CollaborateConfig(AppConfig):
    name = 'collaborate'

    def ready(self):
        import collaborate.signals
