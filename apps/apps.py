from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'



class UsersConfig(AppConfig):
    name = 'apps'

    def ready(self):
        import apps.signals