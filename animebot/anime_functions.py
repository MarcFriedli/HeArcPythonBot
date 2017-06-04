"""
Module permettant la recherche d'informations sur les animes.
Fonctionne selon les instructions passé à la fonction execute_request
"""
import aiohttp
from bs4 import BeautifulSoup

WEB_SITE = 'http://neko-san.fr/'


class AnimeNotFound(Exception):
    """Exception levée quand un anime qui n'existe pas est passé en paramètre."""


class TypeNotFound(Exception):
    """Exception levée quand on cherche un genre qui est inconnu."""


class AnimeNotFree(Exception):
    """Exception levée quand on tente d'accéder à un épisode d'un animé licendié."""


async def get_url(session, url):
    """Return l'url de manière à ce qu'il soit utilisable par bs."""
    async with session.get(url) as response:
        return await response.text()

async def make_soup(session, url):
    """Return la bs de l'URL passé."""
    async with session.get(url) as resp:
        text = await resp.read()
    return BeautifulSoup(text.decode("utf-8"), "html5lib")

async def execute_request(requ, *params):
    """
        Exécute la fonction correspondante à 'requ'.
    """
    async with aiohttp.ClientSession() as session:
        try:
            return await request[requ.lower()](session, *params)
        except AnimeNotFound:
            return "L'anime est introuvable."
        except KeyError:
            return "Instruction inconnue. tapez 'help' pour la liste des instructions."
        except AnimeNotFree:
            return "Cet animé est déjà licencié. Soutenez-le en l'achetant."
        except TypeNotFound:
            return "Genre inconnu."
        except IndexError:
            return "Cet épisode n'existe pas."

async def get_informations(session, anime_name):
    """
        Return les informations sur l'anime passé en argument.
        En revanche, c'est pas très beau à voir...
    """
    soup = await make_soup(session, WEB_SITE+'anime')
    #print(soup.getText)
    for anime_link in soup.find_all('a'):
        for anime_title in anime_link.find_all(attrs='anime-titre'):
            if anime_name.lower() == anime_title.string.lower():
                episodes = []
                author = await get_last_node(anime_link.select('.anime-author td'))
                resume = await get_resume(anime_link.get('href'), session)
                studio = await get_last_node(anime_link.select('.anime-studio td'))
                for episode_ref in anime_link.select('.anime-count span'):
                    episodes.append(episode_ref.string)
                year = anime_link.find(attrs='annee').string
                anime_types = await get_anime_types(anime_link.get('href'), session)
                return f"""Anime "{anime_name}" de {author} par {studio} en {year}.
Genres : {anime_types}.
Résumé : "{resume}" 
Cet anime est composé de {episodes[0]} épisodes,{episodes[1]} OAV et {episodes[2]} films."""
    raise AnimeNotFound

async def get_resume(url, session):
    """Return le résumé de l'anime contenu dans l'URL."""
    soup = await make_soup(session, WEB_SITE + url)
    return soup.find(attrs="resume").string

async def get_anime_types(link, session):
    """Return les genres de l'anime."""
    types = []
    soup = await  make_soup(session, WEB_SITE + link)
    for type in soup.select(".genre"):
        types.append(await get_last_node(type))
    return ", ".join(types)

async def get_last_node(elem):
    """
        Return le dernier noeud d'un élément. Utile quand ledit dernier noeud n'a pas de nom.
    """
    last = ""
    for node in elem:
        last = node.string
    return last if last else ""

async def get_episode(session, anime_name, num_season, num_episode = 0):
    """Return le lien de l'épisode souhaité."""
    soup = await make_soup(session, WEB_SITE + 'anime')
    for anime_link in soup.find_all('a'):
        for anime_title in anime_link.find_all(attrs='anime-titre'):
            if anime_name.lower() == anime_title.string.lower():
                if await get_last_node(anime_link.select(".licencie")) == "Licencié":
                    raise AnimeNotFree
                reply = await found_episode(session, anime_link.get('href'), num_season, num_episode)
                return reply
    raise AnimeNotFound


async def found_episode(session, url, num_season, num_episode):
    """
        Cherche le lien de l'épisode cherché et le return.
    """
    soup = await make_soup(session, WEB_SITE + url)
    season = 1
    episode_with_season = 1
    episode_without_season = 1
    for saison_link in soup.find_all('div', attrs={'class': 'streaming-block'}):
        for saison_name in saison_link.find('h3', attrs={'class': 'streaming-title'}):
            episode_without_season = 1
            for episode_list in saison_link.find_all('a'):
                if (str(season) == str(num_season) and str(episode_with_season) == str(num_episode)) \
                        or (str(episode_without_season) == str(num_season) and str(num_episode) == 0):
                    return episode_list['href']
                else:
                    episode_with_season += 1
                    episode_without_season += 1
            season += 1
        raise IndexError


async def get_anime_after_search(session, *search):
    """Return une liste d'anime répondant à search."""
    soup = await make_soup(session, WEB_SITE + 'anime')
    await is_type_existing(soup, *search)
    result = []
    for anime_link in soup.select('.anime-item'):
        anime_types = await get_anime_types(anime_link.get('href'), session)
        found = True
        for elem in search:
            if elem.lower() not in anime_types:
                found = False
        if found:
            result.append(anime_link.find(attrs='anime-titre').string)
    if not result:
        return "Il n'y a aucun anime qui correspond à votre recherche."
    return "Les animés suivants correspondent à votre recherche :\n" + "\n".join(result)

async def is_type_existing(soup, *types):
    """Vérifie si les genres passés en argument existent dans la base de donnée. Return une exception dans le cas contraire."""
    type_list = []
    for result in soup.select("#anime-genre option"):
        type_list.append(result.string)
    for type in types:
        if type.lower() not in type_list:
            print(type)
            raise TypeNotFound

async def get_instructions(*t):
    """Return les différentes instructions du module ainsi que leur descripiton et comment les utiliser."""
    return f"""Pour avoir les informations sur un anime : info, 'nom_de_l_anime'
-> exemple : info 'Clannad'
Pour obtenir un épisode particulier : episode, 'nom_de_l_anime', num_saison(fac), num_episode
-> exemple : episode, "Elfen Lied", 1, 4
Pour effectuer une recherche selon genre (très lent) : search, valeurs_recherchées
-> exemple : search "comédie" "amour et amitié" """

request = {
    "info": get_informations,
    "episode": get_episode,
    "search": get_anime_after_search,
    "help": get_instructions
}
