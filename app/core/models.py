from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import sys
from utils import scraping_movies
sys.path.append('..')
# Create your models here.
class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self,email,password=None,**extra_fields):
        """Create, save and  return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user=self.model(email=self.normalize_email(email),**extra_fields)
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


class User(AbstractBaseUser,PermissionsMixin):
    """
    User in the system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    filmweb_nick=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD='email'
class Director(models.Model):
    name=models.CharField(max_length=255)
class Movie(models.Model):
    title=models.CharField(max_length=255)
    # action='action'
    # comedy='comedy'
    # drama='drama'
    # fantasy='fantasy'
    # horror='horror'
    # mystery='mystery'
    # romance='romance'
    # thriller='thriller'
    # western='western'
    # genre_choices = ((action,'action'),(comedy,'comedy'),(drama,'drama'),(fantasy,'fantasy'),(horror,'horror'),
    #                  (mystery,'mystery'),(romance,'romance'),(thriller,'thriller'),(western,'western'))
    genre = models.CharField(max_length=255)
    director=models.ForeignKey(Director,on_delete=models.CASCADE)
    year=models.IntegerField()
    description=models.TextField()


class UserTopMovies(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    top_movies=models.ForeignKey(Movie,on_delete=models.CASCADE, default=None,null=True)

@receiver(post_save,sender=User)
def UserProfileCreator(sender, instance=None, created=False, **kwargs):
    if created:
        scraping_movies.adding_to_profile_func(filmweb_nick=instance.filmweb_nick,user=instance)




