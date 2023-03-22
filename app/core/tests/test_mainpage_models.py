from core.models import (Comment, Director, FriendRequest, Movie, Post, Reply,
                         UserProfile)
from core.serializers import MovieSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

MAINPAGE_URL = reverse('core:post-list')

# comments
# directors -> DONE ###
# main_page -> create_post
# movies -> create_movie, list_movies -> DONE ###
# friends -> DONE ###


def create_user(email='test@example.com', password='test123'):
    return get_user_model().objects.create_user(email, password)


def create_movie(**params):
    director, created = Director.objects.get_or_create(name='test_name')

    defaults = {
        'director': director,
        'title': "Movie",
        'genre': "Horror",
        'year': 2147483647,
        'description': "string"
    }
    defaults.update(params)
    movie = Movie.objects.create(**defaults)
    return movie


def create_post(user, **params):
    defaults = {
        "title": "sample_post_title",
        "movie": "sample_movie",
        "text": "sample_description"
    }
    defaults.update(params)
    # post =


class PublicAPITests(TestCase):
    """Tests for unauthenticated user"""

    def setUp(self):
        self.client = APIClient()

    def test_disalow_unauthenitcated(self):
        res = self.client.get(MAINPAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_movie(self):
        payload = {
            'link': 'https://www.filmweb.pl/film/Django-2012-620541'
        }
        res = self.client.post(reverse('core:movie-add-movie'), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_movie_list(self):
        create_movie(title='movie1')
        create_movie(title='movie2')

        res = self.client.get(reverse('core:movie-list'))

        movies = Movie.objects.all().order_by('id')

        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_movie_detail(self):
        create_movie(title='movie1')
        movie = create_movie(title='movie2')

        res = self.client.get(reverse('core:movie-detail', args=[movie.id]))

        serializer = MovieSerializer(movie)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_post(self):
        movie = create_movie()

        payload = {
            "title": "sample_post_title",
            "movie": movie.title,
            "text": "sample_description"
        }
        res = self.client.post(MAINPAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(payload['title'], post.title)
        self.assertEqual(payload['text'], post.text)
        self.assertEqual(movie, post.movie)
        self.assertEqual(post.user, self.user)

    def test_list_directors(self):
        director = Director.objects.create(name='test_name1')
        director = Director.objects.create(name='test_name2')
        res = self.client.get(reverse('core:director-list'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_friend_invite(self):
        friend = create_user(email='friend@example.com')
        friend_client = APIClient()
        friend_client.force_authenticate(friend)

        url = reverse('friend:friends_requests-sending-inv')
        res = friend_client.post(url, {
            "receiver": self.user.id
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['receiver'], self.user.id)
        invites = FriendRequest.objects.all()
        self.assertEqual(len(invites), 1)

        inv = FriendRequest.objects.get(sender=friend, receiver=self.user)
        url = reverse(
            'friend:friends_requests-responding-to-invs', args=[inv.id])
        res = self.client.get(
            url, QUERY_STRING='accept=true')

        up = UserProfile.objects.get(user=self.user)
        self.assertIn(friend, up.friends.all())

    def test_view_friends_posts(self):
        movie = create_movie()

        friend = create_user(email='friend@example.com')
        stranger = create_user(email='stranger@example.com')

        friend_profile = UserProfile.objects.get(user=friend)
        my_profile = UserProfile.objects.get(user=self.user)
        friend_profile.friends.add(self.user)
        my_profile.friends.add(friend)

        Post.objects.create(user=friend, title='friend post',
                            movie=movie, text='test_text')

        Post.objects.create(user=stranger, title='stranger post',
                            movie=movie, text='test_text')

        url = reverse('core:post-list')
        res = self.client.get(url)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # friend = create_user(email='friend.example.com')
    # stranger = create_user(email='stranger.example.com')
