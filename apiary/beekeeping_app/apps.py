from django.apps import AppConfig


class BeekeepingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beekeeping_app'

    def ready(self):
        import beekeeping_app.signals  # Import signals module
