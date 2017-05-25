from urllib import request
from bs4 import BeautifulSoup

soup = BeautifulSoup(request.urlopen('http://neko-san.fr/anime').read().decode('utf-8'), 'html.parser')


def anime_exist(anime):
    """Return true si {anime} est présent dans la base de donnée."""
    for anime_title in soup.find_all(attrs='anime-titre'):
        if(anime == anime_title.string):
            return True
    return False


def find_anime(anime):
    """
        Méthode principale, chercher si {anime} est présent dans la base de données
        Si oui, affiche le nombre d'épisodes et d'OAV
    """
    if anime_exist(anime):
        episods, oav = get_anime_episod_and_oav(anime)


def get_anime_episod_and_oav(anime):
    """Return le nombre d'épisodes et d'OAV de {anime}"""
    episods = 0
    oav = 0
    return episods, oav
