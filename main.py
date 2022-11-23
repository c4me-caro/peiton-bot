import os
import discord
from discord.ext import commands
from config import config
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = str(os.getenv('DISCORD_TOKEN'))

bot = commands.Bot(command_prefix=config.bot_prefix, description=config.DESCRIPTION, activity=discord.Game(name='type {}help'.format(
    config.bot_prefix)), status=discord.Status.online, owner_id=os.getenv('OWNER_ID'), case_insensitive=True, intents=discord.Intents.all())


async def load_extensions():
    for extension in config.initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(str(e))


async def init():
    await load_extensions()
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    print('intializing components...')
    asyncio.run(init())
