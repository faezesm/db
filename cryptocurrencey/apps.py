from django.apps import AppConfig


class CryptocurrenceyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptocurrencey'

    def ready(self):
        from . import signals
