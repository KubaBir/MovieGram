from django.contrib import admin
from .models import Movie, Director, UserTopMovies, User
# Register your models here.
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(UserTopMovies)
admin.site.register(User)
