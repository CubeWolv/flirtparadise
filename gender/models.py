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
        abstract = True  # Make this abstract, no need to reference it directly

# Concrete Profile models
class Guy(Profile):
    pass

class Girl(Profile):
    pass

class Escort(Profile):
    pass

# ProfilePicture model with ForeignKey to concrete profiles
class ProfilePicture(models.Model):
    # ForeignKey to link each picture to a specific guy, girl, or escort
    guy = models.ForeignKey(Guy, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    girl = models.ForeignKey(Girl, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    escort = models.ForeignKey(Escort, related_name="pictures", on_delete=models.CASCADE, null=True, blank=True)
    
    image = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        if self.guy:
            return f"Picture for {self.guy.name}"
        elif self.girl:
            return f"Picture for {self.girl.name}"
        elif self.escort:
            return f"Picture for {self.escort.name}"
        return "Profile Picture"