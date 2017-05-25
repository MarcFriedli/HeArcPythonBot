import aiohttp
from bs4 import BeautifulSoup


class AnimeNotFoundException(Exception):
    """Exception levés quand un anime qui n'existe pas est passé en paramètre"""
    pass

async def get_url(session, url):
    """Return l'url de manière à ce qu'il soit utilisable par bs."""
    async with session.get(url) as response:
        return await response.text()

async def anime_exist(anime, soup):
    """Return le nom de {anime} s'il est trouvé. Lève une exception dans le cas contraire"""
    for anime_title in soup.find_all(attrs='anime-titre'):
        if anime == anime_title.string:
            return anime_title.string
    raise AnimeNotFoundException


async def find_anime(anime):
    """
        Méthode principale, cherche si {anime} est présent dans la base de données
        Si oui, affiche les informations.
    """
    async with aiohttp.ClientSession() as session:
        html = await get_url(session, 'http://neko-san.fr/anime')
        soup = BeautifulSoup(html, 'html5lib')
        try:
            #print(await anime_exist(anime, soup))
            return await anime_exist(anime, soup)
        except AnimeNotFoundException:
            print("L'anime est introuvable.")
            return None


async def get_anime_episod_and_oav(anime):
    """Return le nombre d'épisodes et d'OAV de {anime}."""
    episods = 0
    oav = 0
    return episods, oav
