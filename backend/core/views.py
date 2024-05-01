from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from users.models import CustomUser
from .models import Post
from apis.serializers import PostSerializer

from manage import configured_settings

import sqlite3

@login_required()
def test(request):
    data = dict(sorted(configured_settings.items(), key=lambda x: x[0]))
    if not request.user.is_staff:
        return HttpResponse(status=403)
    return render(request, "test.html", {"data": data})

def filter_posts(location):
    db_file = f"{configured_settings.get('BASE_DIR')}/databases/real_estate.db"
    db = sqlite3.connect(db_file)
    db = db.cursor()
    db.execute(f"SELECT * FROM core_post WHERE location like '%{location.strip()}%'")
    all_data = db.fetchall()
    labels = [i[0] for i in db.description]
    filtered = []
    for i in all_data:
        filtered.append(dict(zip(labels, i)))
    return filtered

@login_required()
def home(request):
    posts = Post.objects.all()
    
    posts = PostSerializer(posts, many=True).data
    posts = [i for i in posts if i["uploader_id"] != request.user.pk] or None
    
    error = None
    if request.method == "GET":
        location = request.GET.get("location")
        if location:
            posts = filter_posts(location)
            if not posts:
                error = f"No such posts about {location!r}."
    
    return render(request, "home.html", {"posts": posts, "error": error})

@login_required()
def my_posts(request):
    posts = Post.objects.filter(uploader_id=request.user.pk)
    return render(request, "my_posts.html", {"posts": posts})

@login_required()
def upload_post(request):
    return render(request, "upload_post.html", {"user": request.user})

@csrf_exempt
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponse(status=404)
    
    uploaded_by_me = post.uploader_id == request.user.pk
    uploader = CustomUser.objects.get(pk=post.uploader_id)
    return render(request, "post_detail.html", {"post": post, "uploader": uploader, "uploaded_by_me": uploaded_by_me})

@login_required()
def setting(request):
    return render(request, "setting.html")

