
import requests
from rest_framework import serializers, status

from .models import Comment, Director, FriendRequest, Movie, Post, UserProfile


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField()

    class Meta:
        model = Movie
        fields = '__all__'
        # read_only_fields = ['director', 'genre', 'year', 'description']


class AddMovieSerializer(serializers.Serializer):
    link = serializers.CharField()

    class Meta:
        model = Movie
        fields = ['link']

    def validate_link(self, attrs):
        response = requests.get(attrs)
        if response.status_code == status.HTTP_400_BAD_REQUEST or not attrs.startswith('https://www.filmweb.pl/film/'):
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
        fields = ['sender', 'receiver']
        read_only_fields = ['sender']


class AcceptingFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['is_active']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'comment_date', 'text']
        extra_kwargs = {
            "user": {"read_only": True},
            "comment_date": {"read_only": True}
        }


class PostCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'post_date', 'title', 'movie', 'text']
        extra_kwargs = {
            "user": {"read_only": True},
            'post_date': {"read_only": True}
        }


class PostListingSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            "user": {"read_only": True},
            'post_date': {"read_only": True}
        }

    def update(self, validated_data):
        comment_data = validated_data.pop('comments')
        post = Post.objects.update(**validated_data)

        for comment in comment_data:
            Comment.objects.create(post=post, **comment)

        return post


class UserProfileSerializer(serializers.ModelSerializer):
    # Return user name instead of id
    user = serializers.CharField()
    posts = PostListingSerializer(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['user', 'top_movies', 'last_watched', 'friends', 'posts']
        read_only_fields = ['user']

    def update(self, validated_data):
        posts_data = validated_data.pop('posts')
        userprofile = UserProfile.objects.update(**validated_data)

        for post in posts_data:
            Post.objects.create(userProfile=userprofile, **post)

        return userprofile
