"""Serializers for the user API View."""
import sys

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

sys.path.append('..')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    filmweb_nick = serializers.CharField(
        allow_null=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'filmweb_nick', 'id']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'filmweb_nick': {'allow_null': True, 'required': False},
            'id': {'allow_null': True, 'required': False}
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authh token."""
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": 'password'}, # input_type: 'password' makes the characters hiddens
                                     trim_whitespace=False,) #trim_whitespace = False in case someone has space on purpose at the end of their password

    def validate(self, attrs):
        """Validate and auth the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
