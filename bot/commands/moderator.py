from discord.ext import commands
from bot.logs import Logger
from discord import Embed, slash_command
from db.objects import MongoGuild
from bot.dialogs import Dialogs

diag = Dialogs()
log = Logger("admin.log", 3)

def is_admin():
  async def predicate(ctx):
    actual_cog = ctx.bot.get_cog("Moderator")
    if not actual_cog:
      return False
    
    roles = await actual_cog.get_admin_roles(ctx.guild.id)
    if len(roles) == 0:
      return ctx.author.guild_permissions.administrator
    
    if any(role.name in roles for role in ctx.author.roles):
      return True
    
    msg = diag.err("NotPermitted")
    if hasattr(ctx, "respond"):
      await ctx.respond(msg, ephemeral=True)
    else:
      await ctx.send(msg)

    return False
  
  return commands.check(predicate)

class Moderator(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    async def get_admin_roles(self, guild_id):
      docs = await self.bot.db.get_document("servers", {"id":guild_id})
      if len(docs) == 0:
        log.warn("No se ha configurado un rol de administración del bot.")
        return []
      
      return docs[0]["admin_role"]
          
    @slash_command(name="embed", description="Genera un embed con los datos requeridos")
    @is_admin()
    async def embed(self, ctx, title, description, image=None):
        docs = await self.bot.db.get_document("servers", {"id": ctx.guild.id})
        if len(docs) == 0:
          log.log("No se ha encontrado instancia del servidor para generar embeds")
          await ctx.respond(diag.err("SystemError"))
          return
        
        doc = docs[0]
        doc.pop("_id", None)
        data = MongoGuild(**doc)

        embed = Embed(
          title=title, description=description, color=data.color if data.color != 0 else ctx.author.color
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_footer(icon_url=data.icon if data.icon != "" else "", text=data.name)

        if image != None:
            embed.set_image(url=image)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Moderator(bot))
