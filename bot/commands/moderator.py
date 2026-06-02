from discord.ext import commands
from bot.logs import Logger
from discord import Embed, slash_command, TextChannel
from db.objects import MongoGuild

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
    
    msg = "Parece que no posees las llaves de esta habitación."
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
        log.warn("No se ha configurado un rol de administración del bot.", metadata=f"System:{guild_id}")
        return []
      
      return docs[0]["admin_role"]
          
    @slash_command(name="embed", description="Genera un mensaje o embed en un canal de texto")
    @is_admin()
    async def embed(self, ctx, title, description, image=None):
        docs = await self.bot.db.get_document("servers", {"id": ctx.guild.id})
        if len(docs) == 0:
          log.log("No se ha encontrado instancia del servidor para generar embeds", metadata=f"{ctx.author.name}:{ctx.guild.name}")
          await ctx.respond("Parece que algo ha fallado. Por favor comunica el error a un administrador.")
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

    @slash_command(name="espera", description="Agrega o elimina un delay o modo lento en canales de texto")
    @is_admin()
    async def slowmode(self, ctx, segundos:int=10):
      if not isinstance(ctx.channel, TextChannel):
        await ctx.respond("Parece que no posees las llaves de esta habitación.", ephemeral=True)
        return

      if segundos < 0 or segundos > 21600:
        await ctx.respond("Introduce un tiempo válido entre 0 y 21600 segundos para esta acción.", ephemeral=True)
        return

      await ctx.channel.edit(slowmode_delay=segundos)

      if segundos == 0:
        await ctx.respond("Se ha desactivado el modo lento.")
      else:
        await ctx.respond("Se ha activado el modo lento.")

def setup(bot):
    bot.add_cog(Moderator(bot))
