import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# User
class User(AbstractUser):
    pass


# Post
class Post(models.Model):
    content = models.CharField(max_length=1200, null=False, blank=False)
    posted_on = models.DateTimeField(default=datetime.datetime.now())
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    # Count likes
    def get_likes(self):
        return self.likes.count()
    
    # Serialize data
    def serialize(self):
        return {
            "content": self.content,
            "posted_on": self.posted_on.strftime("%b %d %Y, %I:%M %p"),
            "posted_by": self.posted_by.username,
            "likes": self.get_likes()
        }
    
    def __str__(self):
        return f"A post created by {self.posted_by} on {self.posted_on}"


# Follower
class Follower(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    
    # Check for valid follow
    def is_valid_follow(self):
        return self.followee != self.follower
    
    def __str__(self):
        return f"{self.follower} follows {self.followee}"


# Comment
class Comment(models.Model):
    text = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.owner} commented on {self.post}"

