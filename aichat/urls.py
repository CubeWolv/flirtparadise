from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('profiles/', views.profiles_list, name='profiles_list'),
    path('chat/profile/<int:profile_id>/', views.chat_with_profile, name='chat_with_profile'),  # Chat with a specific profile


]