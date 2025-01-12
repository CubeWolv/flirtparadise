from django.db import models
from django.utils.timezone import now, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tinymce.models import HTMLField
from django.utils.html import strip_tags
from django.utils.text import slugify

class UserPayment(models.Model):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    payment_status = models.CharField(max_length=20, default="pending")  # pending, success, failed
    status = models.CharField(max_length=20, default="active")  # active, expired
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=1)  # Set expiry time to 24 hours from creation
        super().save(*args, **kwargs)

class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AvailableHour(models.Model):
    time_range = models.CharField(max_length=50)  # E.g., "9 AM - 12 PM"

    def __str__(self):
        return self.time_range

class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Abstract base profile
class Profile(models.Model):
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=255, default="Kampala")
    bio = models.TextField()
    whatsapp = models.CharField(max_length=225)
    services = models.ManyToManyField(Service, blank=True)

    class Meta:
        abstract = True  # Abstract base model

# Concrete profile models
class Guy(Profile):
    pass

class Girl(Profile):
    pass

def get_default_new_until():
    return now() + timedelta(days=14)

class Escort(Profile):
    height = models.CharField(max_length=10, default="Average")
    dress_size = models.CharField(max_length=10, default="Straight")  # Updated default
    skin = models.CharField(max_length=20, default="Fair")
    calls = models.CharField(max_length=20, default="outcalls & incalls")  # Updated default
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)  # Verification status
    is_new = models.BooleanField(default=True)  # New status
    new_until = models.DateTimeField(default=get_default_new_until)  # Use callable function
    hours_available = models.ManyToManyField(AvailableHour, blank=True)
    areas = models.ManyToManyField(Area, blank=True)

# Profile picture model
class ProfilePicture(models.Model):
    guy = models.ForeignKey(Guy, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    girl = models.ForeignKey(Girl, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    escort = models.ForeignKey(Escort, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')  # Provide a default image

    def __str__(self):
        if self.guy:
            return f"Picture for {self.guy.name}"
        elif self.girl:
            return f"Picture for {self.girl.name}"
        elif self.escort:
            return f"Picture for {self.escort.name}"
        return "Profile Picture"

def slug_default():
    # Return the slugified version of the blog title
    return slugify('default-title')  # You can customize this part as needed


class BlogPost(models.Model):
    title = models.CharField(max_length=255)  # Title of the blog post
    slug = models.SlugField(unique=True, default=slug_default)  # Unique slug field
    body = HTMLField()  # Use TinyMCE for rich text editing
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update on save
    published_at = models.DateTimeField(default=now)  # Default to current time
    is_published = models.BooleanField(default=True)  # Toggle visibility

    class Meta:
        ordering = ['-published_at']  # Order by most recent posts first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Generate the slug from the title when saving."""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def snippet(self):
        """Return the first 100 characters of the body as plain text."""
        plain_text = strip_tags(self.body)  # Remove HTML tags
        return f"{plain_text[:1000]}..." if len(plain_text) > 1000 else plain_text