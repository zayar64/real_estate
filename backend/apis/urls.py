from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^users$', views.user_list),
    re_path(r'^posts$', views.post_list),
    re_path(r'^users/(\d+)$', views.user_detail),
    re_path(r'^posts/(\d+)$', views.post_detail),
]
