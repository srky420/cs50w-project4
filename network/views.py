import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follower


"""
Index view
"""
def index(request):
    return render(request, "network/index.html")


"""
Create post view
"""
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


"""
Posts view
"""
def posts(request, filter):
    # Check filter
    if filter == "all":
        posts = Post.objects.all() 
    elif filter == "following" and request.user.is_authenticated:
        
        # Get all posts of current user's followings
        followings = Follower.objects.filter(follower=request.user)
        posts = []
        for f in followings:
            for post in f.followee.posts.all():
                posts.append(post.id)
        
        posts = Post.objects.filter(pk__in=posts)
    else:
        return JsonResponse({"error": "filter not found!"}, status=400)
    
    posts = posts.order_by("-posted_on").all()
    
    # Get page num from args
    page_num = request.GET.get("page")
    
    # Create pagination
    paginator = Paginator(posts, 10)
    posts = paginator.get_page(page_num)
    
    return JsonResponse([post.serialize() for post in posts], safe=False, status=200)
    
    
"""
Profile View
"""
def profile(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "user not found!"}, status=400)
    
    return JsonResponse(user.serialize(), status=200)
    

"""
Login View
"""
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


"""
Logout view
"""
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


"""
Register view
"""
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
