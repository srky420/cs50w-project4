
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create-post"),
    path("followings", views.followings, name="followings"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/<int:user_id>/follow", views.follow, name="follow")
]
