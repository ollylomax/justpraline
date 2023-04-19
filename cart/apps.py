from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Load cart configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
