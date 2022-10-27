from shutil import move

import bs4
import requests


def get_movie(link):
    result = requests.get(link)
    data = bs4.BeautifulSoup(result.text, "lxml")
    movie = {
        'title': None,
        'genre': None,
        'director': None,
        'year': None,
        'description': None
    }
    genres = ['action', 'comedy', 'fantasy', 'thriller', 'horror', 'western',
              'dramat', 'mystery', 'romance', 'melodramat', 'komedia', 'przygodowy', 'dokumentalny',
              'erotyczny', 'sensacyjny', 'obyczajowy', 'wojenny', 'dramat historyczny', 'kryminał',
              'sci-fi', 'dramat obyczajowy', 'gangsterski', 'animacja']

    movie['title'] = data.select('h1.filmCoverSection__title ')[0].getText()
    for a3 in data.find("div", itemprop="genre"):
        if a3.getText().lower().strip() in genres:
            movie['genre'] = a3.getText().lower().strip()
            break
    movie['director'] = data.find("span", itemprop="name").getText()
    movie['year'] = data.select('div.filmCoverSection__year')[0].getText()
    movie['description'] = data.find("span", itemprop="description").getText()

    return movie


# print(get_movie('https://www.filmweb.pl/film/Django-2012-620541'))
