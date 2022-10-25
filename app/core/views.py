from requests import request
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Director, Movie, Post, UserProfile
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


class DirectorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class UserProfileViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    # viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    # def get_serializer_class(self):
    #     if self.method == 'my_profie':
    #         return serializers.MyProfileSerializer
    #     return self.serializer_class

    @ action(methods=["GET", "PATCH"], detail=False, permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        queryset = UserProfile.objects.filter(user=self.request.user).get()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


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
