from django.apps import AppConfig


class VecindadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vecindad'

    def ready(self):
        import vecindad.signals
