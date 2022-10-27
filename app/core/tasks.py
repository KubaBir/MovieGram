from app.celery import app as celery_app
from utils.save_movie import get_movie

from .models import Director, Movie


@celery_app.task
def save_movie_task(link):
    movie = get_movie(link)
    if Director.objects.filter(name=movie['director']).exists():
        director = Director.objects.filter(name=movie['director'])
    else:
        director = Director.objects.create(name=movie['director'])
    movie.pop('director')
    if Movie.objects.get_or_create(director=director, **movie):
        return True
    return False
