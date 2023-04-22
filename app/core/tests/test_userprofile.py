"""Tests for UserProfile Api and model"""

from core.models import UserProfile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.tests.test_user import CREATE_USER_URL, create_user

MY_PROFILE = reverse('core:userprofile-my-profile')


class UserProfileTests(TestCase):
    """Tests the features of user-profile api and user-profile model"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com',
                                password='testpasss',
                                name='TestName',
                                filmweb_nick='michal_kudlinski')
        self.client.force_authenticate(user=self.user)

    def test_user_profile_creation(self):
        """Test if user profile is created upon user creation."""
        self.assertTrue(UserProfile.objects.filter(
            filmweb_nick=self.user.filmweb_nick).exists())

    def test_retrieving_my_user_profile(self):
        """Test if logged in user can retreive their user profile"""
        response = self.client.get(MY_PROFILE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, response.data['user'])
        self.assertEqual(self.user.filmweb_nick, response.data['filmweb_nick'])
