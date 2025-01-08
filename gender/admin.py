from django.contrib import admin
from .models import (
    UserPayment, 
    Guy, 
    Girl, 
    Escort, 
    ProfilePicture, 
    Service, 
    Habit, 
    AvailableHour, 
    Language, 
    Area
)
from django.contrib.contenttypes.admin import GenericTabularInline

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
    filter_horizontal = ('services', 'habits', 'hours_available', 'languages_spoken', 'areas')

# Register additional models
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('time_range',)
    search_fields = ('time_range',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the profile models
admin.site.register(Guy, GuyAdmin)
admin.site.register(Girl, GirlAdmin)
admin.site.register(Escort, EscortAdmin)
