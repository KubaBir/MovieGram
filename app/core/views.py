from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Movie, UserTopMovies, Director
from . import serializers
# Create your views here.

class MoviesListView(ListAPIView):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()

class DirectorListView(ListAPIView):
    serializer_class = serializers.DirectorSerializer
    queryset = Director.objects.all()

class UserTopMoviesListView(ListAPIView):
    serializer_class = serializers.UserTopMoviesSerializer
    queryset = UserTopMovies.objects.all()