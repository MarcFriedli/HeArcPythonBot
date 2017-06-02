"""Bot for Discord."""

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

setup(
    name='AnimeBot_for_Discord',
    version='0.0.1.dev20170601',  # see PEP-0440
    description='A bot for Discord who told information about an anime (in french)',
    python_requires='>=3.5',
    author='Marc Friedli & Julien Feuillade',
    author_email='marc.friedli@he-arc.ch',
    url='https://github.com/MarcFriedli/HeArcPythonBot',
    license='https://opensource.org/licenses/BSD-3-Clause',
    packages=['animebot'],
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest',
        'pytest-aiohttp',
        'pytest-asyncio',
        'pytest-cov'
    )
)