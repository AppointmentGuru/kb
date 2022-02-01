from django.apps import AppConfig


class HelpConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "help"

    def ready(self):
        from .signals import add_to_index
