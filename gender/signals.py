import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Escort, Guy, Girl  # Import all models
from django.conf import settings

def ping_google():
    sitemap_url = f'{settings.SITE_URL}/sitemap.xml'  # Your sitemap URL
    google_ping_url = f'http://www.google.com/ping?sitemap={sitemap_url}'
    try:
        response = requests.get(google_ping_url)
        if response.status_code == 200:
            print("Successfully pinged Google!")
        else:
            print(f"Failed to ping Google: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error pinging Google: {e}")

@receiver(post_save, sender=Escort)
@receiver(post_save, sender=Guy)
@receiver(post_save, sender=Girl)
def notify_google_of_new_post(sender, instance, created, **kwargs):
    """
    This signal is triggered when a new Escort, Guy, or Girl is saved.
    It notifies Google that the sitemap has been updated.
    """
    if created:  # If it's a new post
        ping_google()
    else:  # If it's an update to an existing post
        ping_google()
