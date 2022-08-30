from rest_framework import serializers
from .models import Movie, Director, UserProfile, FriendRequest, Post, Comment
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model= Movie
        fields='__all__'

class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields=['name']


class FriendRequestSerializerList(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['id','timestamp','sender']


class FriendRequestSerializerSend(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields= ['sender','receiver']

class AcceptingFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields= ['is_active']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= ['user','comment_date','text']
        extra_kwargs={
            "user":{"read_only":True},
            "comment_date":{"read_only":True}
        }

class PostCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=['user','post_date','title','movie','text']
        extra_kwargs={
            "user":{"read_only":True},
            'post_date':{"read_only":True}
        }
class PostListingSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True,required=False)
    class Meta:
        model = Post
        fields= '__all__'
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
    posts = PostListingSerializer(many=True,required=False)
    class Meta:
        model = UserProfile
        fields= ['user','top_movies','last_watched','friends','posts']

    def update(self, validated_data):
        posts_data = validated_data.pop('posts')
        userprofile = UserProfile.objects.update(**validated_data)

        for post in posts_data:
            Post.objects.create(userProfile=userprofile, **post)

        return userprofile

