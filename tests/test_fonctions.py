import sys
import os
sys.path.append(os.getcwd())
from animebot import anime_functions
import pytest
import aiohttp


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


# TODO : simplifier ce truc...
@pytest.mark.asyncio
async def test_if_get_last_node_return_the_right_node():
    async with aiohttp.ClientSession() as session:
        soup = await anime_functions.make_soup(session, anime_functions.WEB_SITE + 'anime')
        for anime_link in soup.find_all('a'):
            for anime_title in anime_link.find_all(attrs='anime-titre'):
                if "Higurashi no Naku Koro ni" == anime_title.string:
                    assert await anime_functions.get_last_node(anime_link, 'anime-author') == 'Seventh Expansion'
