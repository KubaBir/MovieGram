from app.celery import app as celery_app
from utils.save_movie import get_movie

from .models import Director, Movie


@celery_app.task
def save_movie_task(link):
    movie = get_movie(link)
    print(movie)
    director,created = Director.objects.get_or_create(name=movie['director'])
    movie.pop('director')
    Movie.objects.get_or_create(director = director, **movie)
    

