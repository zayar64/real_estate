from rest_framework import serializers
from django.utils import timezone
from core.models import Post
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "phone", "address", "image")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "uploader_id", "owner", "property_type", "offer_type", "location", "description", "status", "price", "contact_ph", "uploaded_time")
