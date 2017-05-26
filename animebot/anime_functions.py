"""
Module permettant la recherche d'informations sur les animes.
Fonctionne selon les instructions passé à la fonction execute_request
"""
import aiohttp
from bs4 import BeautifulSoup

WEB_SITE = 'http://neko-san.fr/'


class AnimeNotFoundException(Exception):
    """Exception levés quand un anime qui n'existe pas est passé en paramètre"""
    pass


async def make_soup(session, url):
    """Return la bs de l'URL passé."""
    async with session.get(url) as resp:
        text = await resp.read()
    return BeautifulSoup(text.decode("utf-8"), "html5lib")

async def execute_request(requ, anime=""):
    """
        Méthode principale, cherche si {anime} est présent dans la base de données
        Si oui, affiche les informations.
    """
    async with aiohttp.ClientSession() as session:
        try:
            return await request[requ.lower()](anime, session)
        except AnimeNotFoundException:
            print("L'anime est introuvable.")
            return None
        except KeyError:
            print("Instruction inconnue. tapez 'help' pour la liste des instructions")
            return None

async def get_informations(anime_name, session):
    """
        Return les informations sur l'anime passé en argument
        En revanche, c'est pas très beau à voir...
    """
    soup = await make_soup(session, WEB_SITE+'anime')
    for anime_link in soup.find_all('a'):
        for anime_title in anime_link.find_all(attrs='anime-titre'):
            if anime_name == anime_title.string:
                for anim_author in anime_link.find_all(attrs='anime-author'):
                    for node in anim_author:
                        author = node.string
                resume = await get_resume(anime_link.get('href'), session)
                for anim_studio in anime_link.find_all(attrs='anime-studio'):
                    for node in anim_studio:
                        studio = node.string
                year = anime_link.find(attrs='annee').string
                return f"Anime \"{anime_name}\" de {author} par {studio} en {year}.\nRésumé : \"{resume}\""
    raise AnimeNotFoundException

async def get_resume(url, session):
    """Return le résumé de l'anime contenu dans l'URL"""
    soup = await make_soup(session, WEB_SITE + url)
    return soup.find(attrs="resume").string

async def get_instructions(a, b):
    """Return les différentes instructions du module ainsi que leur descripiton et comment les utiliser"""
    return f"Pour avoir les informations sur un anime : info, nom_de_l_anime"


request = {
    "info": get_informations,
    "help": get_instructions
}
