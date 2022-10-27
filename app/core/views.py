

from multiprocessing import AuthenticationError
from tokenize import Token

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from requests import request
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Comment, Director, Movie, Post, Reply, UserProfile
from .tasks import save_movie_task

# Create your views here.


class MoviesViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action == 'add_movie':
            return serializers.AddMovieSerializer
        return serializers.MovieSerializer

    @action(methods=['POST'], detail=False, url_path='add_movie')
    def add_movie(self, request):
        # queryset = Movie.objects.all()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # task here instead of save
            save_movie_task.delay(request.data['link'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DirectorViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    serializer_class = serializers.DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


@extend_schema_view(
    my_profile=extend_schema(
        parameters=[
            OpenApiParameter(
                'unfriend',
                OpenApiTypes.STR,
                description='Comma seperated list of friend_ids to unfriend'
            ),

        ]
    )
)
class UserProfileViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    # def get_serializer_class(self):
    #     if self.method == 'my_profie':
    #         return serializers.MyProfileSerializer
    #     return self.serializer_class

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    @ action(methods=["GET", "PATCH"], detail=False, permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        obj = UserProfile.objects.filter(user=self.request.user).get()
        unfriend = self.request.query_params.get('unfriend', None)
        if unfriend:
            unfriend_ids = self._params_to_ints(unfriend)
            friends = obj.friends.filter(id__in=unfriend_ids)
            for friend in friends:
                obj.friends.remove(friend)  # a tu nie
                UserProfile.objects.filter(user=friend).get().friends.remove(
                    self.request.user.id)  # czemu tu musi byc id

        queryset = UserProfile.objects.filter(user=self.request.user).get()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# tutaj zmiana na tylko get i retrieve tylko tak zeby dzialal router
class FriendsProfilesViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        my_friends = [el.id for el in UserProfile.objects.filter(
            user=self.request.user).get().friends.all()]
        queryset = UserProfile.objects.filter(user__id__in=my_friends)
        return queryset


# class PostViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.PostSerializer
#     queryset = Post.objects.all()
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def get_queryset(self):
#         return Post.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_serializer_class(self):
#         if self.action == 'add_comment':
#             return serializers.CommentSerializer
#         return serializers.PostSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'directors',
                OpenApiTypes.STR,
                description='Comma seperated list of directors that you are intersted in'
            ),


        ]
    )
)
class MainPageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostListingSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        my_friends = [el.id for el in UserProfile.objects.filter(
            user=self.request.user).get().friends.all()]
        queryset = Post.objects.filter(user__id__in=my_friends)
        directors = self.request.query_params.get('directors')
        if directors:
            try:
                director_ids = []
                for el in directors.split(','):
                    director_ids.append(Director.objects.get(name=el).id)
                queryset = queryset.filter(movie__director__in=director_ids)
            except:
                return queryset

        return queryset

    def create(self, request):
        serializer = serializers.PostCreatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data)


class CommentsViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    serializer_class = serializers.CommentOnPostSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # def list(self,request):
    #     queryset = Comment.objects.filter(user = self.request.user).all()
    #     return queryset

    # def create(self,request):
    #     serializer = self.serializer_class(self.queryset)
    #     if serializer.is_valid():
    #         return Response(serializer.data)
    #     return Response({"Status": "Something went wrong"})
    # def retrieve(self,request):
    #     obj = get_object_or_404
    #     serializer = self.serializer_class(obj)
    #     return Response(serializer.data)


class ReplyViewSet(
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    serializer_class = serializers.ReplyOnCommentSerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
