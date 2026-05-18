from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'products'

    def ready(self):
        # Carga signals.py al arrancar Django para crear UserProfile automaticamente.
        import products.signals  # noqa: F401
