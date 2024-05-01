from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile', views.profile, name='users/profile'),
    path('change_password', views.change_password, name='users/change_password'),
    re_path(r'^(\d+)', views.user_detail, name='user'),
    path('register', views.register, name='users/register'),
    path('login', views.login, name='users/login'),
    path('logout', views.logout, name='users/logout')
]
