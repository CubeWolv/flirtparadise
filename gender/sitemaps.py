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
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Area.objects.all()

    def location(self, obj):
        # Use 'escorts_by_city_major' if there's no sub_city, otherwise 'escorts_by_city'
        if obj.name.lower() == "default-city-name":  # Replace with your default logic
            return reverse('escorts_by_city_major', kwargs={'city': obj.name})
        else:
            return reverse('escorts_by_city', kwargs={'city': obj.name, 'sub_city': 'default-sub-city'})

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['contact', 'flutterwave_payment', 'verify_payment']

    def location(self, item):
        return reverse(item)
