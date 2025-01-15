from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'category', 'views')  # Display relevant fields
    search_fields = ('name', 'category')  # Enable search by name and category

# Register the Profile model with custom settings
admin.site.register(Profile, ProfileAdmin)
