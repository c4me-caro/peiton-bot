from discord.ext import commands
from bot.logs import Logger
from discord import slash_command, Member, PermissionOverwrite
from db.objects import VoiceRooms

log = Logger("tchannels.log", 3)
PrivateChannels = {}
counter = 1

class TemporalChannels(commands.Cog, name="tchanCog"):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(name="roomadd")
  async def add_voice_permission(self, ctx, member: Member):
    if not str(ctx.author.id) in PrivateChannels.keys():
      await ctx.respond("Parece que no has iniciado ninguna sala privada.", ephemeral=True)
      return

    channel = PrivateChannels[str(ctx.author.id)]
    perm_overwrite = PermissionOverwrite()
    perm_overwrite.connect = True
    perm_overwrite.view_channel = True

    await channel.set_permissions(member, overwrite=perm_overwrite)
    await ctx.respond("Usuario agregado al canal.")

  @slash_command(name="roomdel")
  async def delete_voice_permission(self, ctx, member: Member):
    if not str(ctx.author.id) in PrivateChannels.keys():
      await ctx.respond("Parece que no has iniciado ninguna sala privada.", ephemeral=True)
      return

    channel = PrivateChannels[str(ctx.author.id)]
    everyone_overwrite = PermissionOverwrite()
    everyone_overwrite.connect = False
    everyone_overwrite.view_channel = False

    await channel.set_permissions(member, overwrite=everyone_overwrite)
    if member.voice and member.voice.channel.id == channel.id:
      await member.edit(voice_channel=None)

    await ctx.respond("Usuario eliminado del canal.")

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    channel = before.channel
    if channel and channel in PrivateChannels.values():
      if len(channel.members) == 0:
        log.log(f"Se ha eliminado la sala privada {channel.name}", metadata=f"{member.name}:{member.guild.name}")
        await channel.delete()
        del PrivateChannels[str(member.id)]
        counter-=1
      return

    if after.channel == None:
      return

    docs = await self.bot.db.get_document("voiceroom", {"guild_id":member.guild.id})
    if len(docs) == 0:
      return
    
    doc = docs[0]
    doc.pop("_id", None)
    voiceroom = VoiceRooms(**doc)

    if voiceroom.channel == after.channel.id and not str(member.id) in PrivateChannels.keys():
      everyone_overwrite = PermissionOverwrite()
      everyone_overwrite.connect = False
      everyone_overwrite.view_channel = False

      creator_overwrite = PermissionOverwrite()
      creator_overwrite.connect = True
      creator_overwrite.view_channel = True
      creator_overwrite.move_members = True
      creator_overwrite.manage_channels = True
      creator_overwrite.administrator = True
      new_channel = await member.guild.create_voice_channel("Sala privada #"+counter, overwrites={member.guild.default_role: everyone_overwrite, member: creator_overwrite})
      await new_channel.set_permissions(member, overwrite=creator_overwrite)
      PrivateChannels[str(member.id)] = new_channel
      log.log(f"Se ha creado la sala privada {new_channel.name}", metadata=f"{member.name}:{member.guild.name}")

      await member.edit(voice_channel=new_channel)
      counter+=1
      
def setup(bot):
  bot.add_cog(TemporalChannels(bot))
