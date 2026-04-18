from discord.ext import commands
import os
from dotenv import load_dotenv
from bot.logs import Logger
import discord
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
    
    msg = "Me temo que no posees las llaves de esta habitación."
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
      log.log("No se ha configurado un rol de administración del bot.")
      return []
    
    return docs[0]["admin_role"]
      
  @commands.command(name="sync", help="Sincroniza los comandos del bot")
  async def sync(self, ctx):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      log.log(f"{ctx.author.name} ha sincronizado los comandos")
      await self.bot.sync_commands()
      await ctx.send("Se han sincronizado todos los comandos.")
    else:
      await ctx.send("Me temo que no posees las llaves de esta habitación.")

  @commands.command(name="uptime", help="Muestra el tiempo de actividad del bot")
  async def uptime(self, ctx):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      uptime = timedelta(seconds=int(round(time() - self.bot.uptime)))
      await ctx.send(f"El bot ha estado activo por {uptime}.")
    else:
      await ctx.send("Me temo que no posees las llaves de esta habitación.")

  @discord.slash_command(name="load", description="Carga una extensión del bot por nombre corto")
  @is_admin()
  async def load(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.load_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.display_name} ha cargado la extensión {extension}")
      await ctx.respond("La extensión ha sido añadida a las capacidades del bot.")
    else:
      await ctx.respond("Me temo que no posees las llaves de esta habitación.")

  @discord.slash_command(name="unload", description="Inhabilita una extensión del bot por nombre corto")
  @is_admin()
  async def unload(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.unload_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.display_name} ha eliminado la extensión {extension}")
      await ctx.respond("La extensión ha sido eliminada a las capacidades del bot.")
    else:
      await ctx.respond("Me temo que no posees las llaves de esta habitación.")

  @discord.slash_command(name="reload", description="Recarga una extensión del bot por nombre corto")
  @is_admin()
  async def reload(self, ctx, extension: str):
    if str(ctx.author.id) == os.getenv("DISCORD_OWNER"):
      self.bot.reload_extension(f"bot.commands.{extension}")
      log.log(f"{ctx.author.display_name} ha recargado la extensión {extension}")
      await ctx.respond("La extensión ha sido recargada correctamente.")
    else:
      await ctx.respond("Me temo que no posees las llaves de esta habitación.")

  @discord.slash_command(name="ping", description="Comprueba la latencia del bot.")
  @is_admin()
  async def ping(self, ctx):
      await ctx.respond("Pong! {0}".format(round(self.bot.latency, 1)))
       
  @discord.slash_command(name="limpiar", help="Borrar todos los mensajes del canal")
  @is_admin()
  async def limpiar(self, ctx, cantidad: int=1000):
    log.log(f"{ctx.author.display_name} ha limpiado {cantidad} mensajes del canal {ctx.channel}")
    await ctx.channel.purge(limit=cantidad)
    await ctx.respond(f"Se ha borrado todo el historial del canal. (hasta {cantidad} mensajes).", ephemeral=True)

def setup(bot):
  bot.add_cog(Gestion(bot))