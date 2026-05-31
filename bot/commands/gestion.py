from discord.ext import commands
import os
from dotenv import load_dotenv
from bot.logs import Logger
from discord import slash_command
from time import time
from datetime import timedelta

log = Logger("botmanage.log", 3)
load_dotenv()

def is_admin():
  async def predicate(ctx):
    actual_cog = ctx.bot.get_cog("Gestion")
    if not actual_cog:
      return False
    
    roles = await actual_cog.get_admin_roles(ctx.guild.id)
    if len(roles) == 0:
      return ctx.author.guild_permissions.administrator
    
    if any(role.name in roles for role in ctx.author.roles):
      return True
    
    msg = "Parece que no posees las llaves de esta habitación."
    if hasattr(ctx, "respond"):
      await ctx.respond(msg, ephemeral=True)
    else:
      await ctx.send(msg)

    return False
  
  return commands.check(predicate)

class Gestion(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def get_admin_roles(self, guild_id):
    docs = await self.bot.db.get_document("servers", {"id":guild_id})
    if len(docs) == 0:
      log.warn("No se ha configurado un rol de administración del bot.", metadata=f"System:{guild_id}")
      return []
    
    return docs[0]["admin_role"]
      
  @commands.command(name="sync", help="Sincroniza los comandos del bot")
  async def sync(self, ctx):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      log.log(f"{ctx.author.name} ha sincronizado los comandos", metadata=f"{ctx.author.name}:{ctx.guild.name}")
      await self.bot.sync_commands()
      await ctx.send("Se han sincronizado todos los comandos.")
    else:
      await ctx.send("Parece que no posees las llaves de esta habitación.")

  @commands.command(name="uptime", help="Muestra el tiempo de actividad del bot")
  @is_admin()
  async def uptime(self, ctx):
    uptime = timedelta(seconds=int(time() - self.bot.uptime))
    await ctx.send("El bot ha estado activo por {}.".format(uptime))

  @slash_command(name="load", description="Carga una extensión del bot por nombre corto")
  @is_admin()
  async def load(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.load_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.name} ha cargado la extensión {extension}", metadata=f"{ctx.author.name}:{ctx.guild.name}")
      await ctx.respond("La extensión {} ha sido añadida a las capacidades del bot.".format(extension))
    else:
      await ctx.respond("Parece que no posees las llaves de esta habitación.")

  @slash_command(name="unload", description="Inhabilita una extensión del bot por nombre corto")
  @is_admin()
  async def unload(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.unload_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.name} ha eliminado la extensión {extension}", metadata=f"{ctx.author.name}:{ctx.guild.name}")
      await ctx.respond("La extensión {} ha sido eliminada de las capacidades del bot.".format(extension))
    else:
      await ctx.respond("Parece que no posees las llaves de esta habitación.")

  @slash_command(name="reload", description="Recarga una extensión del bot por nombre corto")
  @is_admin()
  async def reload(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.reload_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.namew} ha recargado la extensión {extension}", metadata=f"{ctx.author.name}:{ctx.guild.name}")
      await ctx.respond("La extensión {} ha sido recargada correctamente.".format(extension))
    else:
      await ctx.respond("Parece que no posees las llaves de esta habitación.")

  @slash_command(name="ping", description="Comprueba la latencia del bot.")
  @is_admin()
  async def ping(self, ctx):
      await ctx.respond("Pong! {0}".format(round(self.bot.latency, 1)))
       
  @slash_command(name="limpiar", help="Borrar todos los mensajes del canal")
  @is_admin()
  async def limpiar(self, ctx, cantidad: int=1000):
    log.log(f"{ctx.author.name} ha limpiado {cantidad} mensajes del canal {ctx.channel}", metadata=f"{ctx.author.name}:{ctx.guild.name}")
    await ctx.channel.purge(limit=cantidad)
    await ctx.respond("Se ha borrado el historial del canal. (hasta {} mensajes).".format(cantidad), ephemeral=True)

def setup(bot):
  bot.add_cog(Gestion(bot))