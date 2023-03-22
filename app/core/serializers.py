
import requests
from rest_framework import serializers, status

from .models import (Comment, Director, FriendRequest, Movie, Post, Reply,
                     User, UserProfile)



class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField()

    class Meta:
        model = Movie
        fields = '__all__'


class MovieAddSerializer(serializers.Serializer):
    link = serializers.CharField()
    

    class Meta:
        model = Movie
        fields = ['link']

    def validate_link(self, attrs):
        if not attrs.startswith('https://www.filmweb.pl/film/'):
            raise serializers.ValidationError('Provide filmweb link')
        response = requests.get(attrs)
        if response.status_code != status.HTTP_200_OK:
            raise serializers.ValidationError('Provide filmweb link')
        return attrs


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['name']


class FriendRequestSerializerList(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.name')

    class Meta:
        model = FriendRequest
        fields = ['id', 'timestamp', 'sender']


class FriendRequestSerializerSend(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id','sender','receiver']
        read_only_fields = ['sender']


class ReplyOnCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'user', 'reply_date', 'text', 'comment']
        read_only_fields = ['id', 'user', 'reply_date']


class CommentOnPostSerializer(serializers.ModelSerializer):
    reply_set = ReplyOnCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment_date', 'text', 'post', 'reply_set']
        read_only_fields = ['id', 'user', 'comment_date']


class PostCreateSerializer(serializers.ModelSerializer):
    movie = serializers.CharField()
    user = serializers.CharField(source='user.name', read_only=True)
    comments = CommentOnPostSerializer(
        many=True, required=False, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'comments', 'post_date']

    def create(self, validated_data):
        movie = validated_data.pop('movie')
        movie_instance = Movie.objects.get(title=movie)
        instance = Post.objects.create(movie=movie_instance, **validated_data)
        return instance

    def validate_movie(self, field):
        field = field.capitalize()
        if not Movie.objects.filter(title=field).exists():
            raise serializers.ValidationError('Could not find provided movie.')
        return field


class PostListingSerializer(serializers.ModelSerializer):
    comment_set = CommentOnPostSerializer(many=True, read_only=True)
    movie = serializers.CharField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'post_date',
                  'title', 'movie', 'text', 'comment_set']
        extra_kwargs = {
            "user": {"read_only": True},
            'post_date': {"read_only": True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostListingSerializer(many=True)
    user = serializers.CharField(source='user.name')
    top_movies = serializers.ListField(source='get_top_movies')
    last_watched = serializers.ListField(source='get_last_watched')
    friends = serializers.ListField(source='get_friend_names')

    class Meta:
        model = UserProfile
        fields = ['user','filmweb_nick','top_movies', 'last_watched', 'friends', 'posts']
        

