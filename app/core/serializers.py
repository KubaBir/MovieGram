
from rest_framework import serializers

from .models import User, Comment, Director, FriendRequest, Movie, Post, UserProfile, Reply


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField()

    class Meta:
        model = Movie
        fields = '__all__'


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
class ReplyOnCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id','user','reply_date','text','comment']
        extra_kwargs = {
            "user": {"read_only": True},
            "reply_date" : {"read_only": True},
            "comment" : {"write_only": True}
        }
    def validate(self,data):
        data['user'] = self.context['request'].user
        return data
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id','user','reply_date','text','comment']
        extra_kwargs = {
            "user": {"read_only": True},
            "reply_date" : {"read_only": True},
            "comment": {"read_only": True}
        }



class CommentOnPostSerializer(serializers.ModelSerializer):
    reply_set = ReplyOnCommentSerializer(many = True, read_only = True)
    class Meta:
        model = Comment
        fields = ['id','user', 'comment_date', 'text','post','reply_set']
        extra_kwargs = {
            "user": {"read_only": True},
            "comment_date": {"read_only": True},
            "post" : {"write_only": True}
        }
    def validate(self,data):
        data['user'] = self.context['request'].user
        return data

class CommentSerializer(serializers.ModelSerializer):
    reply_set = ReplyOnCommentSerializer(many = True,read_only = True)
    class Meta:
        model = Comment
        fields = ['id','user', 'comment_date', 'text','post','reply_set']
        extra_kwargs = {
            "user": {"read_only": True},
            "comment_date": {"read_only": True},
            "post": {"read_only": True}
        }
    def validate(self,data):
        data['user'] = self.context['request'].user
        return data


class PostCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'post_date', 'title', 'movie', 'text']
        extra_kwargs = {
            "user": {"read_only": True},
            'post_date': {"read_only": True}
        }
class PostListingSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only = True)
    class Meta:
        model = Post
        fields = ['id','user', 'post_date', 'title', 'movie', 'text','comment_set']
        extra_kwargs = {
            "user": {"read_only": True},
            'post_date': {"read_only": True}
        }



# class CommentingPostSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, required=False)

#     class Meta:
#         model = Post
#         fields = '__all__'
#         extra_kwargs = {
#             "user": {"read_only": True},
#             'post_date': {"read_only": True}
#         }

#     # def update(self, validated_data):
#     #     comment_data = validated_data.pop('comments')
#     #     post = Post.objects.update(**validated_data)

#     #     for comment in comment_data:
#     #         Comment.objects.create(post=post, **comment)

#     #     return post


class UserProfileSerializer(serializers.ModelSerializer):
    # Return user name instead of id
    # user = serializers.CharField()
    posts = PostListingSerializer(many = True)

    class Meta:
        model = UserProfile
        fields = ('user', 'top_movies', 'last_watched', 'friends', 'posts')
        
    
    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def update(self, validated_data):
    #     posts_data = validated_data.pop('posts')
    #     userprofile = UserProfile.objects.update(**validated_data)

    #     for post in posts_data:
    #         Post.objects.create(userProfile=userprofile, **post)

    #     return userprofile






