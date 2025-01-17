from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import  Escort, Area
from .models import Profile

class EscortSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        # Fetch all escorts without filtering by the 'verified' field
        return Escort.objects.all()

    def location(self, obj):
        # Generate the URL for each escort's profile page
        return reverse('view_person', kwargs={'pk': obj.pk})

    def lastmod(self, obj):
        # Optionally, you can return the last modified date
        return obj.new_until  # Last modification date for the escort profile


class ProfileSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Profile.objects.all()

    def location(self, obj):
        return reverse('profile_detail', kwargs={'pk': obj.pk})  # Adjust URL name as needed


class AreaSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Area.objects.all()

    def location(self, obj):
        return reverse('escorts_by_city', kwargs={'city': obj.name})


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['contact', 'escorts', 'flutterwave_payment', 'verify_payment']

    def location(self, item):
        return reverse(item)
