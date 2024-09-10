from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.books'

    # Connect signal receivers
    def ready(self):
        import apps.books.signals
