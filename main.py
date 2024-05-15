import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.logs import Logger

load_dotenv()
log = Logger("general.log", 0)

TOKEN = str(os.getenv('DISCORD_TOKEN'))
PREFIX = "pe/"

extensions = ['general', 'events', 'gestion', 'levels']

bot = commands.Bot(
    command_prefix=PREFIX, 
    description='A savage Peiton learning to be a smart helper.',
    activity=discord.Game(name=f'type {PREFIX}help'), 
    status=discord.Status.online, 
    owner_id=os.getenv('DISCORD_OWNER'),   
    intents=discord.Intents.all()
)

bot.xp_multiplier = 1
bot.initial_max_xp = 2

def load_bot():
    for extension in extensions:
        try:
            bot.load_extension(f'bot.commands.{extension}')
            log.log(f"Se ha cargado la extensión {extension}")
        except Exception as e:
            log.warn(str(e))
    
if __name__ == "__main__":
    load_bot()
    bot.run(TOKEN)