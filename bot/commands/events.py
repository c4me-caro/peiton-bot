from discord.ext import commands
from bot.logs import Logger
from db.objects import MongoGuild, MongoWelcome
from discord import Embed
from discord.errors import CheckFailure
from bot.dialogs import Dialogs

log = Logger("events.log", 3)
diag = Dialogs()

class Events(commands.Cog, name="EventsCog"):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    res = await self.bot.db.intialize_db()
    log.log("Bot Online!") if res else log.error("Base de datos no inicializada.")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    doc = MongoGuild(
      id=guild.id,
      name=guild.name,
      icon=guild.icon.url if guild.icon != None else "",
      admin_role="admin",
      color=guild.owner.color if guild.owner != None else 0
    )

    _ = await self.bot.db.add_document("servers", doc.to_dict())

  @commands.Cog.listener()
  async def on_member_join(self, member):
    docs = await self.bot.db.get_document("welcome", {"guild_id":member.guild.id})
    if len(docs) == 0:
      log.warn("No se ha configurado un canal de bienvenida")
      return
    
    doc = docs[0]
    doc.pop("_id", None)
    data = MongoWelcome(**doc)

    embed = Embed(
      title=diag.msg("welcome").format(member.display_name),
      description=data.description
    )

    if data.image_url != "":
      embed.set_image(url=data.image_url)

    channel = self.bot.get_channel(data.channel)
    if channel == None:
      log.error("Canal de bienvenida no existe o es incorrecto")
      return
    
    embed.color = member.color if data.color == 0 else data.color
    embed.set_footer(icon_url=member.guild.icon.url if member.guild.icon != None else "", text=member.guild.name)
    
    log.log(f"{member.name} se ha unido al servidor {member.guild.name}")
    await channel.send(embed=embed)
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, exception):
    log.warn(exception)
    msg = diag.err("CommandError")

    if type(exception) == commands.errors.CommandNotFound:
      msg = diag.err("CommandNotFound")

    await ctx.send(msg)

  @commands.Cog.listener()
  async def on_application_command_error(self, ctx, exception):
    log.warn(exception)
    if type(exception) == CheckFailure:
      return
    
    await ctx.respond(diag.err("CommandError"))

def setup(bot):
  bot.add_cog(Events(bot))
