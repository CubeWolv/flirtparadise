from django.apps import AppConfig
from django.core.management.base import BaseCommand
import os

class GenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gender'

    def ready(self):
        import gender.signals  # Import your signals here

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from django.contrib.auth import get_user_model  # Import here to ensure the app registry is loaded
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f"Superuser {username} created successfully.")
