import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.logs import Logger
from db.controller import MongoController
from time import time

load_dotenv()
log = Logger("general.log", 0)

TOKEN = str(os.getenv("DISCORD_TOKEN"))
PREFIX = "pe/"

extensions = ["events", "gestion"]

bot = commands.Bot(
  command_prefix=PREFIX, 
  description="bip, bop! A savage Peiton  bot learning to be a smart helper.",
  activity=discord.Game(name=f"type {PREFIX}help"), 
  status=discord.Status.online, 
  owner_id=os.getenv("DISCORD_OWNER"),   
  intents=discord.Intents.all()
)

mongocontroller = MongoController(os.getenv("MONGO_URI"), "discord")
bot.db = mongocontroller
bot.uptime = time()

@bot.command(name="kill")
@commands.is_owner()
async def kill(ctx):
  await ctx.send("🔌 Desconectando servicios y apagando bot...")
  log.log(f"Comando kill ejecutado por {ctx.author}")

  try:
    if hasattr(bot, 'db') and hasattr(bot.db, 'client'):
      bot.db.client.close()
      log.log("Conexión con MongoDB cerrada correctamente.")

  except Exception as e:
    log.warn(f"Error al cerrar MongoDB: {e}")

  await bot.close()

def load_bot():
  for extension in extensions:
    try:
      bot.load_extension(f"bot.commands.{extension}")
      log.log(f"Se ha cargado la extensión {extension}")
    except Exception as e:
      log.warn(str(e))
    
if __name__ == "__main__":
    load_bot()
    try:
      bot.run(TOKEN)
    
    except KeyboardInterrupt:
      log.log("Interrupción ejecutada desde consola")

    finally:
      if not bot.is_closed():
        import asyncio
        asyncio.run(bot.close())