from django.contrib import admin
from .models import Movie, Director, User, FriendRequest, UserProfile, Post, Comment
# Register your models here.
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)

