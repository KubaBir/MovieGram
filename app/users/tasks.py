import time

from app.celery import app as celery_app
from django.contrib.auth import get_user_model
from utils.scraping_movies import adding_to_profile_func, scraping_movies_func


@celery_app.task
def append_movies(filmweb_nick):
    time.sleep(10)
    user = get_user_model().objects.filter(filmweb_nick=filmweb_nick)
    scraping_movies_func(filmweb_nick)
    adding_to_profile_func(filmweb_nick, user)
