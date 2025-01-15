from django.contrib import admin
from .models import (
    UserPayment, 
    Escort, 
    ProfilePicture, 
    Service, 
    AvailableHour, 
    Area,
    BlogPost
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

class EscortAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'city', 'phone_number', 'whatsapp', 'premium', 'verified', 'is_new']
    search_fields = ['name', 'phone_number']
    inlines = [ProfilePictureInline]  # Display ProfilePicture inline
    filter_horizontal = ('services', 'hours_available', 'areas')  # Use filter_horizontal for many-to-many fields

# Register additional models
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('time_range',)
    search_fields = ('time_range',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the Escort model
admin.site.register(Escort, EscortAdmin)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at', 'created_at', 'updated_at')
    list_filter = ('is_published', 'created_at', 'published_at')
    search_fields = ('title', 'body')
    ordering = ('-published_at',)
