import sys

from core import models, serializers
from django.http import HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from rest_framework import generics, status, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins

sys.path.append("..")
# Create your views here.


@extend_schema_view(
    responding_to_invs=extend_schema(
        parameters=[
            OpenApiParameter(
                'accept',
                OpenApiTypes.BOOL,
                description='Do you want to accept this invite? 1-yes, 0-no'
            ),
        
        ]
    )
)
class FriendRequestViewSet( mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for admin """
    serializer_class = serializers.FriendRequestSerializerList
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = models.FriendRequest.objects.all()
        else:
            queryset = models.FriendRequest.objects.filter(
                receiver=self.request.user).all()
        return queryset
    """Actions taking care of users interactions """

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated], serializer_class=serializers.FriendRequestSerializerSend)
    def sending_inv(self, request):
        """function handling sending friends invitation for users"""
        # request.data['sender'] = self.request.user.id
        serializer = serializers.FriendRequestSerializerSend(data=request.data)
        serializer.is_valid(raise_exception=True)
        if models.FriendRequest.objects.filter(sender=self.request.user, receiver=serializer.validated_data['receiver']).exists():
            return Response({"Status": "You have sent this invite already"})
        if serializer.validated_data['receiver'] in models.UserProfile.objects.filter(user=self.request.user).get().friends.all():
            return Response({"Status": "The User is already in your friends "})
        if serializer.validated_data['receiver'] == self.request.user:
            return Response({"Status": "You cant send a user invite to yourself "})
        if models.FriendRequest.objects.filter(sender=serializer.validated_data['receiver'], receiver=self.request.user).exists():
            return Response({"Status": "User has invited you already"})
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(methods = ["GET"], detail = True, permission_classes = [IsAuthenticated])
    def responding_to_invs(self, request,pk= None):
        obj = self.get_object()
        accept = self.request.query_params.get('accept')
        print(accept)
        print('chuj')
        if accept:
            obj.accept()
            obj.delete()
        else:
            obj.decline()
            obj.delete()
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status = status.HTTP_200_OK)
