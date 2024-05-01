from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import CustomUser as User
from core.models import Post
from apis.serializers import UserSerializer

from io import BufferedReader
import os

from manage import configured_settings

def write_image(data, name):
    image_extension = data.name[data.name.index("."):]
    full_name = name+image_extension
    full_path = os.path.join(str(configured_settings.get(BASE_DIR))+"/media/", full_name)
    byte_data = BufferedReader(data.file).read()
    open(full_path, "wb").write(byte_data)
    return full_name

backend = "users.backends.PhoneAuthBackend"

def authenticate_admin(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = auth.authenticate(
            request,
            phone=phone,
            password=password
        )
        error = "Please enter the correct phone number and password for a staff account.\nNote that both fields may be case-sensitive."
        if user is None:
            return render(request, "admin_login.html", {"error": error})
        
        if user is not None:
            if not user.is_staff:
                return render(request, "admin_login.html", {"error": error})
        
        auth.login(request, user, backend=backend)
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
    return render(request, "admin_login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return render(request, "users/register.html", {"error": "Passwords you've entered are not matched!"})

        phone = request.POST.get("phone")
        address = request.POST.get("address")
        
        try:
            user = User.objects.create_user(
                username=username,
                phone=phone,
                password=password1,
                address=address
            )

#            image = request.FILES.get("image")
#            if image:
#                image_name = "profile_images/"+str(user.pk)
#                user.image = write_image(image, image_name)
            
            user.save()
            auth.login(request, user, backend=backend)
            return redirect("home")
        except Exception as e:
            error = "Account with this phone number already exists!"
            error = str(e)
            return render(request, "users/register.html", {"error": error})
        return redirect("users/login")
    return render(request, "users/register.html")

def login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

#        try:
#            User.objects.get(phone=phone)
#        except Exception as e:
#            error = "Account associated with this phone number doesn't exist!"
#            return render(request, "users/login.html", {"error": error})

        user = auth.authenticate(
            request,
            phone=phone,
            password=password
        )
        if user is None:
            error = "Incorrect phone number or password!"
            return render(request, "users/login.html", {"error": error})
        auth.login(request, user, backend=backend)
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect("home")
    return render(request, "users/login.html")

def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required()
def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(uploader_id=user_id)
        return render(request, "users/user_detail.html", {"user": user, "posts": posts})
    except Exception as e:
        return HttpResponse(status=404)

@login_required()
def profile(request):
    user = auth.get_user(request)
    if request.method == "POST":
        password = request.POST.get("password")
        
        if not user.check_password(password):
            return render(request, "users/profile.html", {"user": user, "error": "Incorrect password!"})
        
        user.username = request.POST.get("username")
        user.address = request.POST.get("address")
        
#        image = request.FILES.get("image")
#        if image:
#            image_name = "profile_images/"+str(user.pk)
#            user.image = write_image(image, image_name)

        user.save()

        return redirect("home")
    return render(request, "users/profile.html", {"user": user})

@login_required()
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("oldPassword")
        new_password1 = request.POST.get("newPassword1")
        new_password2 = request.POST.get("newPassword2")
        
        error = None
        user = request.user
        if not user.check_password(old_password):
            error = "Incorrect Old Password!"
        if new_password1 != new_password2:
            error = "New passwords are not matched!"
        if error:
            return render(request, "users/change_password.html", {"error": error})
        user.set_password(new_password1)
        user.save()
        
        user = auth.authenticate(
            username=user.username,
            password=new_password1
        )
        auth.login(request, user)
        return redirect("home")
    return render(request, "users/change_password.html")


