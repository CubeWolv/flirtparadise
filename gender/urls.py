from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('guys', views.guys, name='guys'),
    path('', views.girls, name='girls'),
    path('escorts', views.escorts, name='escorts'),
    path('payment/', views.flutterwave_payment, name='flutterwave_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('save-payment-data/', views.save_payment_data, name='save_payment_data'),
    path('escort/<int:pk>/', views.view_person, name='view_person'),
    path('chat/<int:profile_id>/', views.chat_room, name='chat_room'),
    path('chat/guy/<int:profile_id>/', views.chat_with_guy, name='chatwithguy'),
]