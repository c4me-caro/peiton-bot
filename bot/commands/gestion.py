import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
from bot.logs import Logger

log = Logger("admin.log", 3)
load_dotenv()

class Gestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="sync", help="Sincroniza los comandos del bot")
    @commands.has_any_role('admin supremo')
    async def sync(self, ctx):
        if str(ctx.author.id) == os.getenv('DISCORD_OWNER'):
            await self.bot.sync_commands()
            await ctx.send('Command tree synced.')
        else:
            await ctx.send('Necesitas ser el dueño del bot para ejecutar este comando.')

    @discord.slash_command(name="addrole", description="Añade un rol a un usuario.", guild_ids=['1044359077234479124'])
    @commands.has_any_role('admin supremo', 'staff')
    async def add_role(self, ctx, role, member):
        user = ctx.guild.get_member(
            int(member.replace("<@", "").replace(">", "")))
        if user == None:
            ctx.respond("Este usuario no existe o no se ha podido asignar.")
            return

        rol = get(ctx.guild.roles, name=role)
        if rol == None:
            await ctx.respond("Este rol no existe o no se ha podido agregar.")
            return

        await user.add_roles(rol)
        await ctx.respond("Rol asignado con éxito.")

    @discord.slash_command(name="delrole", description="Elimina un rol a un usuario.", guild_ids=['1044359077234479124'])
    @commands.has_any_role('admin supremo', 'staff')
    async def del_role(self, ctx, role, member):
        user = ctx.guild.get_member(
            int(member.replace("<@", "").replace(">", "")))
        if user == None:
            ctx.respond("Ha ocurrido un error con el usuario.")
            return

        rol = get(ctx.guild.roles, name=role)
        if rol == None:
            await ctx.respond("Este rol no existe o no se ha podido eliminar.")
            return

        await user.remove_roles(rol)
        await ctx.respond("Rol eliminado con éxito.")

    @commands.command(name="clear", help="Vacia los mensajes del canal.")
    @commands.has_any_role('admin supremo', 'staff', 'leader')
    async def clear(self, ctx):
        await ctx.message.channel.purge()

def setup(bot):
    bot.add_cog(Gestion(bot))
