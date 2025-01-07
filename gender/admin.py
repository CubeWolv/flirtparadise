from django.contrib import admin
from .models import UserPayment, Guy, Girl, Escort, ProfilePicture, Service, Habit
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('username', 'payment_status', 'created_at', 'expires_at')
    list_filter = ('payment_status', 'created_at', 'expires_at')
    ordering = ('-created_at',)


class ProfilePictureInline(admin.TabularInline):
    model = ProfilePicture
    extra = 1  # Allows you to add one additional empty row in the admin panel

# Register the profile models with the admin interface
class GuyAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'city', 'gender', 'phone_number', 'whatsapp']
    search_fields = ['name', 'phone_number']
    inlines = [ProfilePictureInline]  # Display ProfilePicture inline

class GirlAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'city', 'gender', 'phone_number', 'whatsapp']
    search_fields = ['name', 'phone_number']
    inlines = [ProfilePictureInline]  # Display ProfilePicture inline

class EscortAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'city', 'gender', 'phone_number', 'whatsapp']
    search_fields = ['name', 'phone_number']
    inlines = [ProfilePictureInline]  # Display ProfilePicture inline

# Register the models with the admin site
admin.site.register(Guy, GuyAdmin)
admin.site.register(Girl, GirlAdmin)
admin.site.register(Escort, EscortAdmin)
admin.site.register(Service)
admin.site.register(Habit)