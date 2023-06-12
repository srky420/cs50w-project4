import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


@login_required
def create_post(request):
    # Ensure POST request
    if request.method != "POST":
        return JsonResponse({"msg": "POST request required!"}, status=400)
    
    # Load json data    
    data = json.loads(request.body)
    
    # Check data has content
    if not data["content"]:
        return JsonResponse({"error": "post has no content!"}, status=400)

    # Create post
    post = Post.objects.create(content=data["content"], posted_by=request.user)
    post.save()
    
    return JsonResponse({"msg": "post created!"}, status=201)


def posts(request, filter):
    # Check filter
    if filter == "all":
        posts = Post.objects.all()
    elif filter == "following":
        pass
    else:
        return JsonResponse({"error": "filter not found!"}, status_code=400) 
    
    posts = posts.order_by("-posted_on").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
        
    
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
