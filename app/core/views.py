from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Director, Movie, Post, UserProfile

# Create your views here.


class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


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
