from discord.ext import bridge, commands
from bot.logs import Logger
from discord import Embed, slash_command, Member
from db.objects import MongoGuild
import random 

log = Logger("general.log", 3)

class General(commands.Cog, name="GeneralCog"):
  def __init__(self, bot):
    self.bot = bot

  @bridge.bridge_command(name="help")
  async def help(self, ctx):
    await ctx.respond("Parece que este comando aún se encuentra en construcción.")

  @slash_command(name='avatar')
  async def avatar(self, ctx, member: Member):
    if member.avatar != "":
      docs = await self.bot.db.get_document("servers", {"id": ctx.guild.id})
      if len(docs) == 0:
        log.log("No se ha encontrado instancia del servidor para generar embeds", metadata=f"{ctx.author.name}:{ctx.guild.name}")
        await ctx.respond("Parece que algo ha fallado. Por favor comunica el error a un administrador.")
        return
      
      doc = docs[0]
      doc.pop("_id", None)
      data = MongoGuild(**doc)
      
      embed = Embed(title="Avatar de @{}".format(member.name), color=data.color if data.color != 0 else ctx.author.color)
      embed.set_image(url=member.avatar)
      embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
      embed.set_footer(icon_url=data.icon if data.icon != "" else "", text=data.name)
      await ctx.respond(embed=embed)
      
    else:
      await ctx.respond("Parece que el usuario seleccionado no posee un avatar que descargar.")

  @slash_command(name='lanzar', description='Cara o sello')
  async def lanzar(self, ctx):
    stat = random. randint(1,100) % 2
    await ctx.respond("Ha salido {}!".format("cara" if stat == 0 else "sello"))

def setup(bot):
  bot.add_cog(General(bot))
