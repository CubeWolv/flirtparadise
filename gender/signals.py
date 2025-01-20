import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BlogPost  # Import BlogPost model
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

@receiver(post_save, sender=BlogPost)
def notify_google_of_new_blog(sender, instance, created, **kwargs):
    """
    This signal is triggered when a new BlogPost is saved or updated.
    It notifies Google that the sitemap has been updated.
    """
    if created and instance.is_published:  # Notify Google only if the blog is newly created and published
        ping_google()
    elif not created and instance.is_published:  # If it's an update to an already published blog
        ping_google()
