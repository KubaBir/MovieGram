from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Movie, UserProfile, Director, Post
from . import serializers
# Create your views here.

class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class DirectorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DirectorSerializer
    queryset = Director.objects.all()
    permission_classes= [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    @action(methods=["GET","PATCH"],detail=False,permission_classes=[IsAuthenticated])
    def my_profile(self,request):
        queryset = UserProfile.objects.filter(user=self.request.user).get()
        serializer=self.get_serializer(queryset)
        return Response(serializer.data)

class FriendsProfilesViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.UserProfileSerializer
    queryset=UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        my_friends=[el.id for el in UserProfile.objects.filter(user=self.request.user).get().friends.all()]
        queryset = UserProfile.objects.filter(user__id__in=my_friends)
        return queryset



