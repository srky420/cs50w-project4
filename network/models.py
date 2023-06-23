import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


"""
User model
"""
class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="images/", default="images/default-profile-pic.jpg")
    
    def get_posts(self):
        posts = self.posts.order_by("-posted_on").all()
        return posts

    def get_followers_count(self):
        return self.followers.count()

    def get_followings_count(self):
        return self.followings.count()


"""
Post model
"""
class Post(models.Model):
    content = models.CharField(max_length=1200, null=False, blank=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def count_likes(self):
        return self.likes.count()

    def get_comments(self):
        return self.comments.all()
    
    def count_comments(self):
        return self.comments.count()
    
    def check_like(self, user):
        try: 
            self.likes.get(pk=user.id)
            return True
        except:
            return False
    
    # Serialize comments
    def serialize_comments(self):
        comments = self.comments.all()
        list = []
        for comment in comments:
            list.append({
                "text": comment.text,
                "owner": comment.owner.username,
                "created": comment.created_on.strftime("%b %d %Y, %I:%M %p")
            })
        return list
    
    # Serialize data
    def serialize(self):
        return {
            "content": self.content,
            "posted_on": self.posted_on.strftime("%b %d %Y, %I:%M %p"),
            "posted_by": {"id": self.posted_by.id, "username": self.posted_by.username},
            "likes": self.get_likes(),
            "comments": list(self.serialize_comments())
        }
    
    def __str__(self):
        return f"A post created by {self.posted_by} on {self.posted_on}"


"""
Follower model
"""
class Follower(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    
    # Check for valid follow
    def is_valid_follow(self):
        return self.followee != self.follower
    
    def __str__(self):
        return f"{self.follower} follows {self.followee}"


"""
Comment model
"""
class Comment(models.Model):
    text = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner} commented on {self.post}"

