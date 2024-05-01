from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import make_password

from rest_framework.parsers import JSONParser

from users.models import CustomUser
from core.models import Post
from .serializers import UserSerializer, PostSerializer

import sqlite3, json

class JsonResponse(HttpResponse):
    def __init__(
        self,
        data,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs,
    ):
        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault("content_type", "application/json")
        data = json.dumps(data, cls=encoder, indent=2, **json_dumps_params)
        super().__init__(content=data, **kwargs)

@csrf_exempt
def user_list(request):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse({"data": serializer.data})
    if request.method == 'POST':
        new_data = JSONParser().parse(request)
        
        password1 = new_data.get("password1")
        password2 = new_data.get("password2")
        if password1 != password2:
            return HttpResponse(status=400, reason="Passwords are not matched!")

        new_data["password"] = make_password(password1)
        serializer = UserSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
    return HttpResponse(status=500)

@csrf_exempt
def user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        new_data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=new_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=400)
    
    if request.method == 'DELETE':
        user.delete()
        posts = Post.objects.filter(uploader_id=user_id)
        posts.delete()
        return HttpResponse(status=204)

@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse({"data": serializer.data})
    if request.method == 'POST':
        new_data = JSONParser().parse(request)
        serializer = PostSerializer(data=new_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return JsonResponse(serializer.data)
            except Exception as e:
                pass
        return HttpResponse(status=500)

@csrf_exempt
def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        new_data = JSONParser(request)
        serializer = PostSerializer(new_data)
        serializer.save()
        return JsonResponse(serializer.data)

    if request.method == 'PATCH':
        new_data = JSONParser().parse(request)
        updated_post = update_post(post, new_data)
        serializer = PostSerializer(updated_post)
        return JsonResponse(serializer.data)
    
    if request.method == 'DELETE':
        post.delete()
        return HttpResponse(204)

