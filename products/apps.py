from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Load products configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
