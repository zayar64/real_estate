from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    phone = models.CharField(max_length=30, unique=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="profile_images/", default="default_image.png")
    REQUIRED_FIELDS = ["phone"]
    
    def __str__(self):
        return f"{self.username} - {self.phone}"
    

