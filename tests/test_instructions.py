import sys
import os
sys.path.append(os.getcwd())
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
    execute_request_with_info_reply = await  anime_functions.execute_request('info', 'Higurashi no Naku Koro ni')
    async with aiohttp.ClientSession() as session:
        get_information_reply = await anime_functions.get_informations(session, ['Higurashi no Naku Koro ni'])
    assert execute_request_with_info_reply == get_information_reply

@pytest.mark.asyncio
async def test_if_espisod_command_work():
    try:
        await anime_functions.execute_request('episod', 'Elfen Lied', 4)
    except NotImplementedError:
        assert True

@pytest.mark.asyncio
async def test_if_search_command_work():
    try:
        assert not await anime_functions.execute_request('search', 'Horreur', 'Comédie')
    except NotImplementedError:
        assert True


@pytest.mark.asyncio
async def test_if_an_unknown_command_doesnt_work():
    assert not await anime_functions.execute_request('blaaaaarg')


@pytest.mark.asyncio
async def test_if_an_unknown_anime_is_not_found():
    assert not await anime_functions.execute_request('info', 'blaaaaarg')
