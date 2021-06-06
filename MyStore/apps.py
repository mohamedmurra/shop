from django.apps import AppConfig


class MystoreConfig(AppConfig):
    name = 'MyStore'

    def ready(self):
        import MyStore.signals
