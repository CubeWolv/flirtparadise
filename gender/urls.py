from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, EscortSitemap, ProfileSitemap, AreaSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'escorts': EscortSitemap,
    'profiles': ProfileSitemap,
    'areas': AreaSitemap,
}

def custom_sitemap_view(request, sitemaps):
    response = sitemap(request, sitemaps)
    response['X-Robots-Tag'] = 'index, follow'
    return response

urlpatterns = [
    path('', views.escorts, name='escorts'),  # For all escorts
    path('escorts-from/<str:city>/<str:sub_city>-escorts/', views.escorts_by_city, name='escorts_by_city'),
    path('escorts-from/<str:city>-escorts/', views.escorts_by_city, name='escorts_by_city_major'),
    path('payment/', views.flutterwave_payment, name='flutterwave_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('save-payment-data/', views.save_payment_data, name='save_payment_data'),
    path('escort/<int:pk>/', views.view_person, name='view_person'),  # Generic profile view
    path('blog/', views.blog, name='blog'),
    path('sitemap.xml', custom_sitemap_view, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('<slug:blog_title>/', views.viewblog, name='viewblog'),
]
