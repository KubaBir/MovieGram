import sys

from core import models, serializers
from django.http import HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

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
    ),
    invitations_sent_by_me=extend_schema(
        parameters=[
            OpenApiParameter(
                'unsend',
                OpenApiTypes.STR,
                description='Which friend requests do you want to unsend? (comma seperated list of ids)'
            ),

        ]
    )
)
class FriendRequestViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for admin """
    serializer_class = serializers.FriendRequestSerializerList
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = models.FriendRequest.objects.all()
        if self.action == 'invitations_sent_by_me':
            queryset = models.FriendRequest.objects.filter(
                sender=self.request.user).all()
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
            return Response({"Status": "You have sent this invite already"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['receiver'] in models.UserProfile.objects.filter(user=self.request.user).get().friends.all():
            return Response({"Status": "The User is already in your friends "}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['receiver'] == self.request.user:
            return Response({"Status": "You cant send a user invite to yourself "}, status=status.HTTP_400_BAD_REQUEST)
        if models.FriendRequest.objects.filter(sender=serializer.validated_data['receiver'], receiver=self.request.user).exists():
            return Response({"Status": "User has invited you already"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True, permission_classes=[IsAuthenticated])
    def responding_to_invs(self, request, pk=None):
        obj = self.get_object()
        accept = self.request.query_params.get('accept')
        if accept == 'true':
            obj.accept()
            obj.delete()
        else:
            obj.decline()
            obj.delete()
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated], serializer_class=serializers.FriendRequestSerializerList)
    def invitations_sent_by_me(self, request):
        unsend = self.request.query_params.get('unsend', None)
        if unsend:
            unsend_ids = self._params_to_ints(unsend)
            friend_reqs = models.FriendRequest.objects.filter(
                id__in=unsend_ids)
            for friend_req in friend_reqs:
                models.FriendRequest.objects.filter(id=friend_req.id).delete()

        queryset = models.FriendRequest.objects.filter(
            sender=self.request.user).all()
        serializer = self.get_serializer(queryset, many=True)

        print(models.FriendRequest.objects.filter(
            sender=self.request.user)[0].sender)
        return Response(serializer.data, status=status.HTTP_200_OK)
