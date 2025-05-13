from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, AreaSitemap, BlogSitemap

# Define the sitemaps
sitemaps_dict = {
    'static': StaticViewSitemap,
    'areas': AreaSitemap,
    'blogs': BlogSitemap,
}

urlpatterns = [
    path('', views.escorts, name='escorts'),  # All escorts
    path('escorts-from/<city>/', views.escorts_by_city_major, name='escorts_by_city_major'),
    path('escorts-from/<city>/<sub_city>/', views.escorts_by_city, name='escorts_by_city'),
    path('payment/', views.flutterwave_payment, name='flutterwave_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('save-payment-data/', views.save_payment_data, name='save_payment_data'),
    path('escort/<int:pk>/', views.view_person, name='view_person'),
    path('blog/', views.blog, name='blog'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps_dict}, name='sitemap'),
    path('<slug:blog_title>/', views.viewblog, name='viewblog'),
]
