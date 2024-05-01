from django.db import models
from django.utils import timezone

class Post(models.Model):
    uploader_id = models.IntegerField()
    owner = models.CharField(max_length=30)
    property_type = models.CharField(max_length=50)
    offer_type = models.CharField(max_length=50)
    location = models.TextField()
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=150)
    price = models.IntegerField()
    contact_ph = models.CharField(max_length=15)
    uploaded_time = models.DateTimeField(default=timezone.datetime.now())
    
    def __str__(self):
        return f"( {self.property_type} ) {self.location}"

