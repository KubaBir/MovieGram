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

sys.path.append("..")
# Create your views here.


@extend_schema_view(
    my_invs=extend_schema(
        parameters=[
            OpenApiParameter(
                'accept',
                OpenApiTypes.STR,
                description='Comma seperated list of ids to accept'
            ),
            OpenApiParameter(
                'decline',
                OpenApiTypes.STR,
                description="Comma seperated list of ids to decline"
            )
        ]
    )
)
class FriendRequestViewSet(viewsets.GenericViewSet):
    """View for admin """
    serializer_class = serializers.FriendRequestSerializerList
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            queryset = models.FriendRequest.objects.all()
        else:
            queryset = models.FriendRequest.objects.filter(
                receiver=self.request.user).all()
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
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def my_invs(self, request):
        queryset = models.FriendRequest.objects.filter(
            receiver=self.request.user).all()
        accept = self.request.query_params.get('accept')
        decline = self.request.query_params.get('decline')
        if accept:
            accept_ids = self._params_to_ints(accept)
            qs = queryset.filter(id__in=accept_ids)
            for obj in qs:
                obj.accept()
                obj.delete()
        if decline:
            decline_ids = self._params_to_ints(decline)
            qs = queryset.filter(id__in=decline_ids)
            for obj in qs:
                obj.decline()
                obj.delete()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
