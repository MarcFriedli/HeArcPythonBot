from animebot import anime_methods
import pytest


def test_website_is_right():
    """Vérification que la connexion au site est bien faite."""
    assert "<title>Neko-san - Une infinité d'animes en streaming</title>" == str(anime_methods.soup.title)


def test_if_an_existing_anime_is_found():
    """Vérification qu'un anime se trouvant dans la base de donnée est trouvé"""
    assert anime_methods.anime_exist("Higurashi no Naku Koro ni")


def test_if_an_inexisting_anime_is_not_found():
    """Vérification qu'un mot ne se trouvant pas dans la base de donnée n'est pas trouvé"""
    assert not anime_methods.anime_exist("Blaaaaaarg")

test_website_is_right()
test_if_an_existing_anime_is_found()
test_if_an_inexisting_anime_is_not_found()