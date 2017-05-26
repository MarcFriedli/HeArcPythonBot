from animebot import anime_functions
import pytest
import aiohttp


@pytest.mark.asyncio
async def test_if_get_resume_work():
    """Vérification que le résumé soit le bon..."""
    async with aiohttp.ClientSession() as session:
        assert await anime_functions.get_resume('anime/higurashi-no-naku-koro-ni') == "L’histoire se déroule en 1983, dans un " \
                "petit village du nom de Hinamizawa. Keiichi Maebara, un jeune garçon, vient de déménager, et il doit " \
                "intégrer la seule école du coin, où tous les âges se croisent dans une seule et même classe… " \
                "Rapidement, il va se faire de nouvelles amies : Rena, Satoko, Mion et Rika. Keiichi va également " \
                "apprendre l’effrayante histoire de Hinamizawa, une histoire d’horribles meurtres liés plus ou moins " \
                "au projet de barrage dans le village. Malheureusement pour lui, il semblerait que ses nouvelles amies " \
                "cachent elles-mêmes un très lourd secret à ce sujet…"

