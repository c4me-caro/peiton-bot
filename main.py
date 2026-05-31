import os
import discord
from discord.ext import bridge
from dotenv import load_dotenv
from bot.logs import Logger
from db.controller import MongoController
from web.server import run_app
import asyncio

load_dotenv()
log = Logger("system.log", 2)

TOKEN = str(os.getenv("DISCORD_TOKEN"))
PREFIX = "p/"

extensions = ["events", "gestion", "moderator", "general", "tchannel"]

bot = bridge.Bot(
  command_prefix=PREFIX, 
  description="bip, bop! A savage Peiton bot learning to be a smart helper.",
  activity=discord.Game(name=f"type {PREFIX}help"), 
  status=discord.Status.online, 
  owner_id=os.getenv("DISCORD_OWNER"),
  intents=discord.Intents.all(),
  help_command=None
)

mongocontroller = MongoController(os.getenv("MONGO_URI"), "discord")
bot.db = mongocontroller

def load_bot():
  for extension in extensions:
    try:
      bot.load_extension(f"bot.commands.{extension}")
      log.log(f"Se ha cargado la extensión {extension}")
    except Exception as e:
      log.warn(str(e))

async def stop():
  if hasattr(bot, "db") and hasattr(bot.db, "client"):
    bot.db.client.close()
    log.log("Conexión con MongoDB cerrada correctamente.")

  if not bot.is_closed():
    await bot.close()

async def main():
  load_bot()

  try:
    await asyncio.gather(run_app(bot), bot.start(TOKEN))
  
  except:
    pass

  finally:
    await stop()

if __name__ == "__main__":
  try:
    asyncio.run(main())
  
  except KeyboardInterrupt:
    log.warn("Interrupción de teclado generada.")

  except Exception as e:
    log.error(str(e))
  