from discord.ext import commands
from bot.logs import Logger
from bot.dialogs import Dialogs
import discord
from db.objects import MongoGuild
import random 

log = Logger("general.log", 3)
diag = Dialogs()

class General(commands.Cog, name="GeneralCog"):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command(name="help")
  async def help(self, ctx):
    docs = await self.bot.db.get_document("servers", {"id": ctx.guild.id})
    if len(docs) == 0:
      log.log("No se ha encontrado instancia del servidor para generar embeds")
      await ctx.respond(diag.err("SystemError"))
      return
    
    doc = docs[0]
    doc.pop("_id", None)
    data = MongoGuild(**doc)

    embed = discord.Embed(title=diag.hlp("helpTitle"), color=data.color if data.color != 0 else ctx.author.color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
    embed.set_footer(icon_url=data.icon if data.icon != "" else "", text=data.name)

    embed.add_field(name=diag.hlp("generalHelpTitle"), value=diag.hlp("generalHelpText"), inline=False)
    embed.add_field(name=diag.hlp("technicalHelpTitle"), value=diag.hlp("technicalHelpText"), inline=False)
    embed.add_field(name=diag.hlp("aboutHelpTitle"), value=diag.hlp("aboutHelpText"), inline=False)
    await ctx.respond(embed=embed)

  @discord.slash_command(name='avatar')
  async def avatar(self, ctx, member_id):
    try:
      member_id = member_id.replace("<@", "").replace(">", "")
      member = await self.bot.fetch_user(member_id)
      
      if member.avatar != "":
        docs = await self.bot.db.get_document("servers", {"id": ctx.guild.id})
        if len(docs) == 0:
          log.log("No se ha encontrado instancia del servidor para generar embeds")
          await ctx.respond(diag.err("SystemError"))
          return
        
        doc = docs[0]
        doc.pop("_id", None)
        data = MongoGuild(**doc)
        
        embed = discord.Embed(title=diag.msg("avatar").format(member.name), color=data.color if data.color != 0 else ctx.author.color)
        embed.set_image(url=member.avatar)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_footer(icon_url=data.icon if data.icon != "" else "", text=data.name)
        await ctx.respond(embed=embed)
        
      else:
        await ctx.respond(diag.err("UserAvatar"))
            
    except Exception as e:
      await ctx.respond("Error: {}".format(e))
      return

  @discord.slash_command(name='lanzar', description='Cara o sello')
  async def lanzar(self, ctx):
    stat = random. randint(1,100) % 2
    await ctx.respond("Ha salido {}!".format("cara" if stat == 0 else "sello"))

def setup(bot):
  bot.add_cog(General(bot))
