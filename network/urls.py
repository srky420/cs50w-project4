
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
    path("profile/<int:user_id>/follow", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("comment/delete/<int:comment_id>", views.delete_comment, name="delete_comment")
]
