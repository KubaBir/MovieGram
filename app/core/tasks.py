from django.contrib.auth import get_user_model
from utils.save_movie import get_movie

from app.celery import app as celery_app

from .models import Director, Movie, MovieWatch, UserProfile


@celery_app.task
def save_movie_task(link, user_id):
    movie = get_movie(link)
    director, created = Director.objects.get_or_create(name=movie['director'])
    movie.pop('director')
    movie, created = Movie.objects.get_or_create(director=director, **movie)

    user = get_user_model().objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)

    # last_watched = user_profile.last_watched.order_by('-date')
    # print(last_watched)

    watch_instance = MovieWatch.objects.create(movie=movie)

    user_profile.last_watched.add(watch_instance)
    user_profile.save()

    return True
