from django.test import TestCase
from users.models import CustomUser
from django.contrib import auth

class UserTest(TestCase):
    
    def test_register_and_login(self):
        username = "Zayar Minn"
        phone = "09771864713"
        password = "junian"
        
        CustomUser.objects.create_user(
            username=username,
            phone=phone,
            password=password
        )
        
        user = auth.authenticate(
            phone=phone,
            password=password
        )
        self.assertEqual(username, user.username)
