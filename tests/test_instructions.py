from animebot import anime_functions
import pytest
import aiohttp

@pytest.mark.asyncio
async def test_if_help_command_work():
    assert await anime_functions.execute_request('help') == await anime_functions.get_instructions('a', 'b')


@pytest.mark.asyncio
async def test_if_help_command_with_all_case_work():
    assert await anime_functions.execute_request('hElp') == await anime_functions.get_instructions('a', 'b')


@pytest.mark.asyncio
async def test_if_info_command_work():
    async with aiohttp.ClientSession() as session:
        assert await anime_functions.execute_request('info', 'Higurashi no Naku Koro ni') \
               == \
               await anime_functions.get_informations('Higurashi no Naku Koro ni', session)


@pytest.mark.asyncio
async def test_if_an_unknown_command_doesnt_work():
    assert not await anime_functions.execute_request('blaaaaarg')


@pytest.mark.asyncio
async def test_if_an_unknown_anime_is_not_found():
    assert not await anime_functions.execute_request('info', 'blaaaaarg')
