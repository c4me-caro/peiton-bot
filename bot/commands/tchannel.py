from discord.ext import commands
from bot.logs import Logger
from bot.dialogs import Dialogs
import discord

log = Logger("tchannels.log", 3)
diag = Dialogs()
PrivateChannels = {}

class TemporalChannels(commands.Cog, name="tchanCog"):
  def __init__(self, bot):
    self.bot = bot

  @discord.slash_command(name="sala", description="Crear un canal de voz temporal como sala privada")
  async def crear_sala(self, ctx, nombre: str):
    if str(ctx.author.id) in PrivateChannels:
      await ctx.respond(diag.msg("CreateAudioRoomError"))
      return

    everyone_overwrite = discord.PermissionOverwrite()
    everyone_overwrite.connect = False
    everyone_overwrite.view_channel = False

    creator_overwrite = discord.PermissionOverwrite()
    creator_overwrite.connect = True
    creator_overwrite.view_channel = True
    creator_overwrite.move_members = True
    creator_overwrite.manage_channels = True
    creator_overwrite.administrator = True
    new_channel = await ctx.guild.create_voice_channel(nombre, overwrites={ctx.guild.default_role: everyone_overwrite, ctx.author: creator_overwrite})
    await new_channel.set_permissions(ctx.author, overwrite=creator_overwrite)

    PrivateChannels[str(ctx.author.id)] = new_channel
    log.log(f"Se ha creado la sala privada {new_channel.name}")

    await ctx.respond(diag.msg("createAudioRoom").format(new_channel.mention))

  @discord.slash_command(name="")

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    channel = before.channel
    if PrivateChannels[str(member.id)] == channel:
      if len(channel.members) == 0:
        log.log(f"Se ha eliminado la sala privada {channel.name}")
        await channel.delete()
        del PrivateChannels[str(member.id)]

def setup(bot):
  bot.add_cog(TemporalChannels(bot))
