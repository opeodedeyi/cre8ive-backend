from django.apps import AppConfig


class ShowcaseConfig(AppConfig):
    name = 'showcase'

    def ready(self):
        import showcase.signals
