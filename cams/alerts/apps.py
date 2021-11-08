from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'


class DetectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detects'
