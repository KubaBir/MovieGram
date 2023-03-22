"""Tests for friendrequest model and interaction between useprofile model and friendrequest model"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from users.tests.test_user import create_user, CREATE_USER_URL
from core.tests.test_userprofile import MY_PROFILE
from core.models import UserProfile
from django.utils.http import urlencode
from rest_framework.response import Response

SEND_INV_URL = reverse('friend:friends_requests-sending-inv')
MY_INVS = reverse('friend:friends_requests-list')

def responding_to_invs_url(friend_request_id):
    """create and return a responding to set invitation url"""
    return reverse('friend:friends_requests-responding-to-invs',args = [friend_request_id])
class FriendSystemTests(TestCase):
    """Test class for friends system"""
    
    def setUp(self):
        self.client = APIClient()
        self.client1 = APIClient()
        self.first_user = create_user(email = 'user1@example.com',
                                password = 'testpasss',
                                name = 'User1')
        self.second_user = create_user(email = 'user2@example.com',
                                  password = 'testpasss1',
                                  name = 'User2',
                                  filmweb_nick = 'michal_kudlinski')
        self.client.force_authenticate(user=self.first_user)
        self.client1.force_authenticate(user=self.second_user)
    
    def test_sending_invitation(self):
        """Test if sending invitation works between users"""
        payload = { 'receiver': self.second_user.id}
        self.client.post(SEND_INV_URL,payload)

        res = self.client1.get(MY_INVS)
        self.assertEqual(res.data[0]['sender'], self.first_user.name)
    
    def test_accepting_a_friend_request(self):
        """Test accepting a friend request on the responding_to_invs endpoint"""
        payload = { 'receiver': self.second_user.id}
        self.client.post(SEND_INV_URL,payload)
        url = responding_to_invs_url(1)
        url1 = '{}?{}'.format(url, urlencode({'accept':'true'}))

        res2 = self.client1.get(url1)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        res3 = self.client1.get(MY_INVS)
        self.assertEqual(len(res3.data),0)
      
        UserProfile.refresh_from_db(self.second_user)
        self.assertIn(self.first_user , UserProfile.objects.filter(user = self.second_user).get().friends.all())  
    
    def test_unfriending_a_friend(self):
        """Testing unfriending a friend from a UserProfile """
        payload = { 'receiver': self.second_user.id}
        self.client.post(SEND_INV_URL,payload)
        url = responding_to_invs_url(1)
        url1 = '{}?{}'.format(url, urlencode({'accept':'true'}))
        res2 = self.client1.get(url1)
        unfriend_url = '{}?{}'.format(MY_PROFILE, urlencode({'unfriend':'1'}))
        res = self.client1.get(unfriend_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res1 = self.client1.get(MY_PROFILE)
        self.assertNotIn(self.first_user,res1.data['friends'])



    def test_declining_a_friend_request(self):
        """Test declining a friend request from responding_to_inv endpoint"""
        payload = { 'receiver': self.second_user.id}
        self.client.post(SEND_INV_URL,payload)
        url = responding_to_invs_url(2)
        url1 = '{}?{}'.format(url, urlencode({'accept':'false'}))

        res2 = self.client1.get(url1)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        res3 = self.client1.get(MY_INVS)
        self.assertEqual(len(res3.data),0)
    
        self.assertNotIn(self.first_user , UserProfile.objects.filter(user = self.second_user).get().friends.all())  
    
    def test_sending_the_same_request_twice(self):
        """Test sending the same request twice returns a error message"""
        payload = { 'receiver': self.second_user.id}
        res1 = self.client.post(SEND_INV_URL,payload)
        res2 = self.client.post(SEND_INV_URL,payload)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.data,{'Status': 'You have sent this invite already'})
        res3 = self.client1.get(MY_INVS)
        self.assertEqual(len(res3.data),1)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_sending_friend_request_when_friend_already_in_your_list(self):
        """Test sending friend request to a friend already in your list returning a error message"""
        payload = { 'receiver': self.second_user.id}
        res1 =self.client.post(SEND_INV_URL,payload)
        url = responding_to_invs_url(3)
        url1 = '{}?{}'.format(url, urlencode({'accept':'true'}))
        res2 = self.client1.get(url1)
        res3 = self.client.post(SEND_INV_URL,payload)
        self.assertEqual(res3.data,{"Status": "The User is already in your friends "}) 
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_sending_friend_request_to_yourself(self):
        """Test sending a frien request to yourself returns a error message"""
        payload = { 'receiver': self.first_user.id}
        res1 =self.client.post(SEND_INV_URL,payload)
        self.assertEqual(res1.data, {"Status": "You cant send a user invite to yourself "})
        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_sending_friend_request_when_you_have_been_invited_already(self):
        """Test sending a friend request to user that has invited you already returns a error message"""
        payload = { 'receiver': self.first_user.id}
        res1 =self.client1.post(SEND_INV_URL,payload)
        payload1= { 'receiver': self.second_user.id}
        res2 = self.client.post(SEND_INV_URL,payload1)
        self.assertEqual(res2.data,{"Status": "User has invited you already"} )
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
    


    
    
    

        

        


        
        




        
        

