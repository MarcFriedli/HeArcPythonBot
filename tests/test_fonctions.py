import sys
import os
sys.path.append(os.getcwd())
from animebot import anime_functions
import pytest
import aiohttp

@pytest.mark.asyncio
async def test_if_get_episode_with_season_and_episode_return_the_right_link():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_episode(session, "Elfen LieD", 1, 9)
    assert reply == "http://neko-san.fr/streaming/elfen-lied-09-vostfr"

@pytest.mark.asyncio
async def test_if_get_episode_with_only_episode_reutnr_the_right_link():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_episode(session, "Elfen LieD", 9)
    assert reply == "http://neko-san.fr/streaming/elfen-lied-09-vostfr"

@pytest.mark.asyncio
async def test_if_get_episode_with_an_licencied_episode_dosent_return_a_link():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_episode(session, "Angel Beats!", 1, 4)
    assert reply == "Cet animé est déjà licencié. Soutenez-le en l'achetant."

@pytest.mark.asyncio
async def test_if_get_episode_with_an_inexisting_espisode_dosent_work():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_episode(session, "Elfen Lied", 1, 17)
    assert reply == "Cet épisode n'existe pas."


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_anime_after_search_with_inexisting_types_raise_an_exception():
    async with aiohttp.ClientSession() as session:
        try:
            await  anime_functions.get_anime_after_search(session, "totoro")
        except anime_functions.TypeNotFound:
            assert True


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_anime_after_search_with_too_much_types_found_nothing():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_anime_after_search(session, "Comédie", "Horreur", "Romance", "Action", "Sport")
    assert reply == "Il n'y a aucun anime qui correspond à votre recherche."


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_anime_after_search_work():
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_anime_after_search(session, "Amour et amitié", "Horreur", "Ecchi")
    assert reply == "Les animés suivants correspondent à votre recherche : Bokusatsu Tenshi Dokuro-chan"


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_is_type_existing_found_existings_types():
    async with aiohttp.ClientSession() as session:
        soup = await anime_functions.make_soup(session, anime_functions.WEB_SITE + 'anime')
        try:
            anime_functions.is_type_existing(soup, "Comédie", "Amour et amitié")
        except anime_functions.TypeNotFound:
            return False


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_is_type_raise_a_TypeNotFound_exeption_with_an_inexisting_type():
    async with aiohttp.ClientSession() as session:
        soup = await anime_functions.make_soup(session, anime_functions.WEB_SITE + 'anime')
        try:
            anime_functions.is_type_existing(soup, "Comédie", "Horrreur")
        except anime_functions.TypeNotFound:
            assert True


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_resume_work():
    """Vérification que le résumé soit le bon..."""
    async with aiohttp.ClientSession() as session:
        assert await anime_functions.get_resume('anime/higurashi-no-naku-koro-ni',
                                                session) == "L’histoire se déroule en 1983, dans un " \
                                                            "petit village du nom de Hinamizawa. Keiichi Maebara, un jeune garçon, vient de déménager, et il doit " \
                                                            "intégrer la seule école du coin, où tous les âges se croisent dans une seule et même classe… " \
                                                            "Rapidement, il va se faire de nouvelles amies : Rena, Satoko, Mion et Rika. Keiichi va également " \
                                                            "apprendre l’effrayante histoire de Hinamizawa, une histoire d’horribles meurtres liés plus ou moins " \
                                                            "au projet de barrage dans le village. Malheureusement pour lui, il semblerait que ses nouvelles amies " \
                                                            "cachent elles-mêmes un très lourd secret à ce sujet…"


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_anime_type_work():
    """Vérification que lorsqu'on passe un paramètre, on trouve les bons genres"""
    async with aiohttp.ClientSession() as session:
        reply = await anime_functions.get_anime_types("anime/abarenbou-rikishi-matsutarou", session)
        assert reply.lower() == "sport"


@pytest.mark.skip
@pytest.mark.asyncio
async def test_if_get_last_node_return_the_right_node():
    async with aiohttp.ClientSession() as session:
        soup = await anime_functions.make_soup(session, anime_functions.WEB_SITE + 'anime')
        for anime_link in soup.find_all('a'):
            for anime_title in anime_link.find_all(attrs='anime-titre'):
                if "Higurashi no Naku Koro ni" == anime_title.string:
                    reply = await anime_functions.get_last_node(anime_link.select('.anime-author td'))
                    print(reply)
                    assert reply == 'Seventh Expansion'
