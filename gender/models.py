from django.db import models
from django.utils.timezone import now, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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

class Habit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AvailableHour(models.Model):
    time_range = models.CharField(max_length=50)  # E.g., "9 AM - 12 PM"

    def __str__(self):
        return self.time_range

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Abstract base profile
class Profile(models.Model):
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    bio = models.TextField()
    whatsapp = models.CharField(max_length=225)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    services = models.ManyToManyField(Service, blank=True)
    habits = models.ManyToManyField(Habit, blank=True)

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
    dress_size = models.CharField(max_length=10, default="M")  # Example sizes: S, M, L, etc.
    skin = models.CharField(max_length=20, default="Fair")
    calls = models.CharField(max_length=20, default="Fair")
    premium = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)  # Verification status
    is_new = models.BooleanField(default=True)  # New status
    new_until = models.DateTimeField(default=get_default_new_until)  # Use callable function
    likings = models.TextField(blank=True, default="None")
    dislikes = models.TextField(blank=True, default="None")
    hours_available = models.ManyToManyField(AvailableHour, blank=True)
    languages_spoken = models.ManyToManyField(Language, blank=True)
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