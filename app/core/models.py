import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.tasks import append_movies
from utils import scraping_movies

sys.path.append('..')
# Create your models here.


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and  return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    filmweb_nick = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Director(models.Model):
    name = models.CharField(max_length=255)
    wiki_link = models.URLField(max_length=255, default=None, null=True)

    def save(self, *args, **kwargs):
        # funkcja odpowiedzialna za generowanie linku do wikipedii danego rezysera
        try:
            link_name = self.name.replace(' ', '_')
            self.wiki_link = f'https://pl.wikipedia.org/wiki/{link_name}'

            super().save(*args, **kwargs)
        except:
            print('Could not find director wiki page.')

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        receiver_friend_list = UserProfile.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = UserProfile.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """Receiver cancels"""
        self.is_active = False
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    text = models.TextField()
    rate = models.IntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(10)])
    comments = models.ManyToManyField(Comment, default=None, blank=True)

    def __str__(self):
        return f"{self.user.name}, {self.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user")
    filmweb_nick = models.CharField(max_length=255)
    top_movies = models.ManyToManyField(Movie, default=None)
    last_watched = models.ManyToManyField(
        Movie, default=None, related_name='last_watched')
    friends = models.ManyToManyField(
        User, blank=True, related_name="friends")
    posts = models.ManyToManyField(Post, default=None)

    def __str__(self):
        return self.user.name

    def add_friend(self, account):

        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)


@ receiver(post_save, sender=User)
def UserProfileCreator(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, filmweb_nick = instance.filmweb_nick)

        if instance.filmweb_nick != '':
            # scraping_movies.adding_to_profile_func(
            #     filmweb_nick=instance.filmweb_nick, user=instance)
            append_movies.delay(
                filmweb_nick=instance.filmweb_nick)
