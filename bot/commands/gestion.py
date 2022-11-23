from discord.ext import commands
from config import config
from bot import utils
from discord.utils import get
import asyncio


class Gestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set_confess', help='Establece el canal de confesiones.', aliases=['set_confesar', 'confesschannel'])
    @commands.has_role('admin supremo')
    async def _set_confess(self, ctx, channel: str):
        channel = channel.replace('<#', '').replace('>', '')
        try:
            channel = ctx.guild.get_channel(int(channel))
            config.confess_channel = channel.id

            await utils.message_embed(ctx, "Canal de confesiones establecido!")
            print("Se ha establecido el canal {} para confesiones.".format(channel))

        except Exception as e:
            print(str(e))
            await utils.alert_embed(ctx, 'ID de canal no válida.')
            return

    @commands.command(name='set_autorole', help='Establece el canal de autoroles.', aliases=['set_autorol', 'autorolechannel'])
    @commands.has_role('admin supremo')
    async def _set_autorole(self, ctx, channel: str):
        channel = channel.replace('<#', '').replace('>', '')
        try:
            channel = ctx.guild.get_channel(int(channel))
            config.autorole_channel = channel.id

            await utils.message_embed(ctx, "Canal de autoroles establecido!")
            print("Se ha establecido el canal {} para autoroles.".format(channel))

        except Exception as e:
            print(str(e))
            await utils.alert_embed(ctx, 'ID de canal no válida.')
            return

    @commands.command(name="nuevorol", help="Añade un rol a un usuario.", aliases=["addrole", "roleadd", "giverole"])
    @commands.has_any_role('admin supremo', 'staff')
    async def _new_role(self, ctx, rol: str, user: str):
        member = ctx.guild.get_member(
            int(user.replace("<@", "").replace(">", "")))
        if member == None:
            print("Ha ocurrido un error con el usuario.")
            return

        role = get(ctx.guild.roles, name=rol)
        if role == None:
            await utils.alert_embed(ctx, "Este rol no existe o no se ha podido agregar.")
            return

        await member.add_roles(role)

    @commands.command(name="quitarrol", help="Elimina un rol a un usuario.", aliases=["delrole", "roledel", "removerole"])
    @commands.has_any_role('admin supremo', 'staff')
    async def _quit_role(self, ctx, rol: str, user: str):
        member = ctx.guild.get_member(
            int(user.replace("<@", "").replace(">", "")))
        if member == None:
            print("Ha ocurrido un error con el usuario.")
            return

        role = get(ctx.guild.roles, name=rol)
        if role == None:
            await utils.alert_embed(ctx, "Este rol no existe o no se ha podido eliminar.")
            return

        await member.remove_roles(role)

    @commands.command(name="autorole", help="Crea un mensaje para autoroles.", aliases=["createautorol", "newautorole"])
    @commands.has_any_role('admin supremo', 'staff')
    async def _autocreate(self, ctx, message, inicio: int, final: int = -1):
        try:
            emojis = config.autorol_corespondence.keys()
            emojis = list(emojis)
            emojis = emojis[inicio:final]
        except Exception as e:
            print(str(e))
            await utils.alert_embed(ctx, "el inicio y el final son incorrectos")
            return

        channel = config.autorole_channel
        if channel == '':
            await utils.alert_embed(ctx, "El canal de confesiones no ha sido establecido")
            return

        channel_obj = self.bot.get_channel(int(channel))

        msg = await channel_obj.send(message)
        config.autorol_messages.append(str(msg.id))

        for i in emojis:
            await msg.add_reaction(i)

    @commands.command(name="clear", help="Vacia los mensajes del canal.")
    @commands.has_any_role('admin supremo', 'staff', 'leader')
    async def _purgue_channel(self, ctx):
        await ctx.message.channel.purge()
            

async def setup(bot):
    await bot.add_cog(Gestion(bot))
