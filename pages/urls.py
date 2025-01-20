from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('contactus', views.contact, name='contact'),
    path('sitemap/' ,views.sitemap ,name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

]