from rest_framework import serializers
from .models import Movie, Director, UserTopMovies
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model= Movie
        fields='__all__'

class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields=['name']

class UserTopMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopMovies
        fields='__all__'