from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female'), ('bi', 'Bi-sexual')])
    category = models.CharField(max_length=255)
    description = models.TextField()
    api_model = models.CharField(max_length=255)
    prompts = models.TextField()
    views = models.IntegerField(default=0)  # New field to track the number of views
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # New image field
    pay = models.BooleanField(default=False)  # Checkbox for payment status

    def __str__(self):
        return self.name
