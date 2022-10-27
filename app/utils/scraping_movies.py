import sys

import bs4
import requests
from core import models

sys.path.append('..')


def adding_to_profile_func(filmweb_nick, user):
    top_filmy = []
    result = requests.get(
        "https://www.filmweb.pl/user/{}".format(filmweb_nick))
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
            movie.append(a3.getText().lower().strip())
            break

        for a4 in soup1.find("span", itemprop="name"):
            movie.append(a4.getText())
        for a5 in soup1.select('div.filmCoverSection__year'):
            movie.append(a5.getText())
        for a6 in soup1.find("span", itemprop="description"):
            movie.append(a6.getText())
        suma = 0
        filmy.append(movie)

    gatunki = {"akcja": ['sensacyjny', 'wojenny', 'kryminał', 'gangsterski', 'fantasy', 'akcja', "western", "true crime", "sztuki walki", 'szpiegowski', 'film-noir'],
               "przygodowy": ['przygodowy', 'familijny'], "romans": ["erotyczny", "romans", "XXX"], "dramat": ["obyczajowy", 'melodramat', 'dramat obyczajowy', 'dramat historyczny',
                                                                                                               'kostiumowy', 'psychologiczny', 'dramat', 'surrealistyczny', 'sportowy', 'religijny', 'dramat sądowy'], "animacja": ['animacja', 'anime', 'animacja dla dorosłych'], 'sci-fi': ['sci-fi'],
               'komedia': ['komedia', 'satyra', 'komedia rom.', 'komedia obycz.', 'komedia kryminalna', 'groteska filmowa', 'czarna komedia'],
               'krotkometrazowy': ['krótkometrażowy'], "horror": ['horror'], "thriller": ["thriller"], "dokumentalny": ["dokumentalny", 'przyrodniczy', 'historyczny', 'dokumentalizowany'],
               "swiateczny": ['świąteczny'], 'polityczny': ['propagandowy', 'polityczny'], 'artystyczny': ['poetycki', 'muzyczny', 'musical']}

    for el in filmy:
        if models.Director.objects.filter(name=el[2]).exists() == False:
            models.Director.objects.create(
                name=el[2], wiki_link='https://nic.com')
        if models.Movie.objects.filter(title=el[0]).exists() == False:
            gatunek = ''
            found = False
            for key, val in gatunki.items():
                if el[1] in val:
                    found = True
                    gatunek = key
            if not found:
                gatunek = 'inne'
            models.Movie.objects.create(title=el[0], genre=gatunek, director=models.Director.objects.get(name=el[2]),
                                        year=el[3], description=el[4])
        obj = models.Movie.objects.get(title=el[0])
        models.UserProfile.objects.get(user=user).top_movies.add(obj)
