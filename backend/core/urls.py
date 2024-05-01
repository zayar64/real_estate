from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('setting', views.setting, name='setting'),
    path('test', views.test),
    path('my-posts', views.my_posts, name='my-posts'),
    re_path(r'^posts/(\d+)$', views.post_detail, name='post'),
    path('upload-post', views.upload_post)
]
