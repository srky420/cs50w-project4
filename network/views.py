import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.timesince import timesince

from .models import User, Post, Follower, Comment


"""
Index view
"""
def index(request):
    # Get all posts
    posts = Post.objects.all()
    posts = posts.order_by("-posted_on")
    
    paginator = Paginator(posts, 10)
    
    page_num = request.GET.get("page")
    
    posts = paginator.get_page(page_num if page_num else 1)
    
    # Create zipped list for likes and posts
    likes = []
    for post in posts:
        likes.append(post.check_like(user=request.user))
    
    zipped_list = zip(posts, likes)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "zipped_list": zipped_list
    })


"""
Followings view
"""
@login_required
def followings(request):
    # Get followings list
    followings = Follower.objects.filter(follower=request.user)
    
    # Create a list of post ids using followings list
    posts = []
    for f in followings:
        for post in f.followee.posts.all():
            posts.append(post.id)    

    # Get post objects using post ids list
    posts = Post.objects.filter(pk__in=posts)
    posts = posts.order_by("-posted_on")
    
    paginator = Paginator(posts, 10)
    
    page_num = request.GET.get("page")
    
    posts = paginator.get_page(page_num if page_num else 1)
    
    # Create zipped list for likes and posts
    likes = []
    for post in posts:
        likes.append(post.check_like(user=request.user))
        
    zipped_list = zip(posts, likes)
    
    return render(request, "network/index.html", {
        "zipped_list": zipped_list,
        "posts": posts
    })


"""
Create post view
"""
@login_required(redirect_field_name="login")
def create_post(request):
    # Ensure POST request
    if request.method == "POST":
        content = request.POST["content"]

        if not content:
            return HttpResponseRedirect(reverse("index"))
        
        post = Post.objects.create(content=content, posted_by=request.user)
        post.save()
        
        return HttpResponseRedirect(reverse("index"))
    
    
"""
Profile View
"""
def profile(request, user_id):
    # Try to get user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    # Get all posts of user
    posts = user.get_posts()
    posts = posts.order_by("-posted_on")
    
    # Create pagination
    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    posts = paginator.get_page(page_num if page_num else 1)
    
    # Create zipped list for like and post
    likes = []
    for post in posts:
        likes.append(post.check_like(user=request.user))
        
    zipped_list = zip(posts, likes)

    is_following = False
    try:
        if (request.user.is_authenticated):
            Follower.objects.get(followee=user, follower=request.user)
            is_following = True
    except Follower.DoesNotExist:
        is_following = False

    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "zipped_list": zipped_list,
        "is_following": is_following
    })


"""
Like func
"""
@login_required
def like(request, post_id):
    # Try to get post 
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found!"}, status=400)
        
    # Toggle like
    if post.check_like(user=request.user):
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        "msg": "Like toggled!", 
        "liked": liked,
        "likes_count": post.count_likes()
        }, status=201)
    

"""
Follow func
"""
@login_required
def follow(request, user_id):
    # Try to get user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist!"}, status=400)
    
    # Try to get follower, else create new
    try:
        follower = Follower.objects.get(followee=user, follower=request.user)
        follower.delete()
        follow = False
        
    except Follower.DoesNotExist:
        follower = Follower.objects.create(followee=user, follower=request.user)

        if not follower.is_valid_follow():
            follower.delete()
            return JsonResponse({"error": "Invalid follow!"}, status=400)

        follower.save()
        follow = True
        
    return JsonResponse({
        "msg": "Follow toggled!", 
        "follow": follow,
        "followers_count": user.get_followers_count(),
        "followings_count": request.user.get_followings_count()
        }, status=201)


"""
Edit post func
"""
@login_required
def edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required!"}, status=400)
    
    # Try to get post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)
    
    # Ensure user validity
    if post.posted_by != request.user:
        return JsonResponse({"error": "Post edit forbidden"}, status=403)
    
    # Load request's body
    data = json.loads(request.body)
    
    if not data.get("content"):
        return JsonResponse({"error": "Content required!"}, status=400)
    
    # Update post's content
    post.content = data["content"]
    post.save()
    
    return HttpResponse(status=204)


"""
Comment func
"""
@login_required
def comment(request, post_id):
    # Ensure POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required!"}, status=400)
    
    # Try to get post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist!"}, status=400)
    
    # Load request body
    data = json.loads(request.body)
    
    if not data.get("comment"):
        return JsonResponse({"error": "Comment not found!"}, status=400)

    comment = Comment.objects.create(text=data["comment"], owner=request.user, post=post)
    comment.save()
    
    return JsonResponse({
        "msg": "Comment created!", 
        "profile_pic_url": request.user.profile_pic.url, 
        "username": request.user.username,
        "user_id": request.user.id, 
        "comment": comment.text,
        "comment_id": comment.id,
        "created_on": timesince(comment.created_on),
        "comments_count": post.count_comments()}, status=201)


"""
Delete comment func
"""
@login_required
def delete_comment(request, comment_id):
    # Try to get comment obj
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"msg": "Comment does not exist!"}, status=400)
    
    # Check if comment's owner is the request's user
    if comment.owner != request.user:
        return JsonResponse({"error": "Comment deletion forbidden"}, status=403)
    
    comment.delete()
    
    return JsonResponse({
        "msg": "Comment deleted!",
        "comments_count": comment.post.count_comments()
        }, status=201)


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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        profile_pic = None
        if request.FILES.get("profilepic"):
            profile_pic = request.FILES["profilepic"]

        if not username or not email or not password or not confirmation:
            return render(request, "network/register.html", {
                "message": "Input fields required."
            })

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if profile_pic is not None:
                user = User.objects.create_user(username, email, password, profile_pic=profile_pic)
            else:
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
