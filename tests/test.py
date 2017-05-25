from animebot import anime_functions
import pytest


@pytest.mark.asyncio
async def test_if_an_existing_anime_is_found():
    """Vérification qu'un anime se trouvant dans la base de donnée est trouvé"""
    assert str(await anime_functions.find_anime("Zettai Shonen")) == "Zettai Shonen"


@pytest.mark.asyncio
async def test_if_an_inexisting_anime_is_not_found():
    """Vérification qu'un mot ne se trouvant pas dans la base de donnée n'est pas trouvé"""
    assert not await anime_functions.find_anime("Blaaaaaarg")