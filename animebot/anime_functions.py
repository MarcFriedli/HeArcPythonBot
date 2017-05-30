"""
Module permettant la recherche d'informations sur les animes.
Fonctionne selon les instructions passé à la fonction execute_request
"""
import aiohttp
from bs4 import BeautifulSoup

WEB_SITE = 'http://neko-san.fr/'


class AnimeNotFoundException(Exception):
    """Exception levée quant un anime qui n'existe pas est passé en paramètre"""
    pass


class AnimeLicenciedException(Exception):
    """Exception levée quand on tente d'accéder à un épisode d'un animé licendié"""
    pass


async def make_soup(session, url):
    """Return la bs de l'URL passé."""
    async with session.get(url) as resp:
        text = await resp.read()
    return BeautifulSoup(text.decode("utf-8"), "html5lib")

async def execute_request(requ, *param):
    """
        Exécute la fonction correspondante à 'requ'
    """
    async with aiohttp.ClientSession() as session:
        try:
            return await request[requ.lower()](session, param)
        except AnimeNotFoundException:
            print("L'anime est introuvable.")
            return None
        except KeyError:
            print("Instruction inconnue. tapez 'help' pour la liste des instructions")
            return None
        except AnimeLicenciedException:
            print("Cet animé est déjà licencié. Soutenez-le en l'achetant.")

async def get_informations(session, anime_name):
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
    """Return le résumé de l'anime contenu dans l'URL."""
    soup = await make_soup(session, WEB_SITE + url)
    return soup.find(attrs="resume").string

async def get_episode(session, anime_name,  num_episod):
    """Return le lien de l'épisode choisi"""
    return "Not implemented yet."

async def get_anime_after_search(session, search):
    """Return une liste d'anime répondant à search"""
    return "Not implemented yet."

async def get_instructions(*t):
    """Return les différentes instructions du module ainsi que leur descripiton et comment les utiliser"""
    return f"Pour avoir les informations sur un anime : info, nom_de_l_anime\n" \
           f"Pour obtenir un épisode particulier : episod, nom_de_l_anime, num_episode\n" \
           f"Pour effectuer une recherche : search, type_de_recherche(genre/auteur), valeurs_recherchées"


request = {
    "info": get_informations,
    "episod": get_episode,
    "search": get_anime_after_search,
    "help": get_instructions
}
