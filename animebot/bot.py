"""
Bot pour discord.
"""
import discord
from animebot import anime_functions
from discord.ext import commands
import configparser

# Prefix à mettre devant les mots pour que le bot les reconnais
commands = commands.Bot(command_prefix="!")


# Fonction pour dire que le bot est logué
@commands.event
async def on_ready():
    print('Logged in')
    print('Name :{}'.format(commands.user.name))
    print('ID : {}'.format(commands.user.id))
    print(discord.__version__)


# Pour tester si le bot répond
@commands.command()
async def ping(*args):
    await commands.say('Pong!')


# Exécute la requête demandée
@commands.command()
async def request(requ, *args):
    await commands.say("Requête en cours... L'opération peut prendre du temps (surtout pour la recherche)...")
    await commands.say(str(await anime_functions.execute_request(requ, *args)))

config = configparser.ConfigParser()
config.read('../config.ini')
token = config['animebot']['TOKEN']

commands.run(token)

