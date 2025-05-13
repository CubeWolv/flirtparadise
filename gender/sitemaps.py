from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Area, BlogPost

class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        # Include only published blog posts
        return BlogPost.objects.filter(is_published=True)

    def location(self, obj):
        return reverse('viewblog', kwargs={'blog_title': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

class AreaSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Area.objects.all()  # Fetch all areas

    def location(self, obj):
        # Normalize the area name and create URLs for both city and sub-city
        parts = [part.strip().lower().replace(' ', '-') for part in obj.name.split(',')]

        if len(parts) == 1:
            # Only city: link to the major city view
            return reverse('escorts_by_city_major', kwargs={'city': parts[0]})
        elif len(parts) == 2:
            # City + Sub-city: link to full city/sub-city page
            return reverse('escorts_by_city', kwargs={'city': parts[0], 'sub_city': f"{parts[1]}-escorts"})
        else:
            # Handle invalid or unexpected data
            return '/'

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['escorts','blog','contact', 'flutterwave_payment', 'verify_payment']

    def location(self, item):
        return reverse(item)
