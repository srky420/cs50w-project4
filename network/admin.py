from django.contrib import admin

from .models import User, Post, Follower, Comment


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "posted_by", "content", "posted_on")
    filter_horizontal = ("likes",)


class FollowerAdmin(admin.ModelAdmin):
    list_display = ("followee", "follower")
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "owner", "post")
    

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Comment, CommentAdmin)
