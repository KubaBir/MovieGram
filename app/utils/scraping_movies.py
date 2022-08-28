import bs4
import requests
import sys
sys.path.append('..')
import time
from core import models
def scraping_movies_func(filmweb_nick):
    top_filmy = []
    result = requests.get("https://www.filmweb.pl/user/{}".format(filmweb_nick))
    soup = bs4.BeautifulSoup(result.text, "lxml")
    for a in soup.select('.filmPoster__filmLink', href=True):
        if len(top_filmy) < 6:
            top_filmy.append(a['href'])
        else:
            pass

    print(top_filmy)

    filmy = []
    for el in top_filmy:
        movie = []
        result1 = requests.get("https://www.filmweb.pl{}".format(el))
        soup1 = bs4.BeautifulSoup(result1.text, "lxml")
        for a2 in soup1.select('h1.filmCoverSection__title'):
            movie.append(a2.getText())
        for a3 in soup1.find("div", itemprop="genre"):
            if a3.getText().lower().strip() in ['action', 'comedy', 'fantasy', 'thriller', 'horror', 'western',
                                                'dramat','mystery', 'romance', 'melodramat', 'komedia', 'przygodowy','dokumentalny',
                                                'erotyczny','sensacyjny','obyczajowy','wojenny','dramat historyczny','kryminał',
                                                'sci-fi','dramat obyczajowy','gangsterski','animacja']:
                movie.append(a3.getText().lower().strip())
                break

        for a4 in soup1.find("span", itemprop="name"):
            movie.append(a4.getText())
        for a5 in soup1.select('div.filmCoverSection__year'):
            movie.append(a5.getText())
        for a6 in soup1.find("span", itemprop="description"):
            movie.append(a6.getText())

        filmy.append(movie)

    for el in filmy:
        if models.Director.objects.filter(name=el[2]).exists() == False:
            models.Director.objects.create(name=el[2])
        if models.Movie.objects.filter(title=el[0]).exists() == False:
            models.Movie.objects.create(title=el[0], genre=el[1], director=models.Director.objects.filter(name=el[2]).get(),
                                 year=el[3], description=el[4])


def adding_to_profile_func(filmweb_nick,user):
        time.sleep(3)
        top_filmy = []
        result = requests.get("https://www.filmweb.pl/user/{}".format(filmweb_nick))
        soup = bs4.BeautifulSoup(result.text, "lxml")
        for a in soup.select('.filmPoster__filmLink', href=True):
            if len(top_filmy) < 6:
                top_filmy.append(a['href'])
            else:
                pass

        print(top_filmy)

        filmy = []
        for el in top_filmy:
            movie = []
            result1 = requests.get("https://www.filmweb.pl{}".format(el))
            soup1 = bs4.BeautifulSoup(result1.text, "lxml")
            for a2 in soup1.select('h1.filmCoverSection__title'):
                movie.append(a2.getText())
            for a3 in soup1.find("div", itemprop="genre"):
                if a3.getText().lower().strip() in ['action', 'comedy', 'fantasy', 'thriller', 'horror', 'western',
                                                    'dramat','mystery', 'romance', 'melodramat', 'psychologiczny',
                                                    'komedia','kostiumowy','przygodowy','erotyczny','dokumentalny','sensacyjny',
                                                    'obyczajowy','wojenny', 'dramat historyczny','kryminał','sci-fi','dramat obyczajowy',
                                                    'gangsterski','animacja']:
                    movie.append(a3.getText().lower().strip())
                    break

            for a4 in soup1.find("span", itemprop="name"):
                movie.append(a4.getText())
            for a5 in soup1.select('div.filmCoverSection__year'):
                movie.append(a5.getText())
            for a6 in soup1.find("span", itemprop="description"):
                movie.append(a6.getText())
            suma=0



            filmy.append(movie)
        for el in filmy:
            obj = models.Movie.objects.filter(title=el[0]).get()
            models.UserTopMovies.objects.create(user=user,top_movies=obj)















