from django.apps import AppConfig


class BaseDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.base_data'
