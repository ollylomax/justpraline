from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Load contact configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
