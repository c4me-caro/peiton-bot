import discord
from discord.ext import commands
from discord import Embed
from bot.logs import Logger

log = Logger("commands.log", 3)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='ping', description="Comprueba la latencia del bot.", guild_ids=['1044359077234479124'])
    async def ping(self, ctx):
        await ctx.respond('Pong! {0}'.format(round(self.bot.latency, 1)))

    @discord.slash_command(name='avatar', description="Muestra tu avatar o el de otra persona", guild_ids=['1044359077234479124'])
    async def avatar(self, ctx, member_id):
        try:
            member_id = member_id.replace("<@", "").replace(">", "")
            member = await self.bot.fetch_user(member_id)
            if member.avatar != "":
                embed = Embed(
                    title='@{}\'s avatar'.format(member.name), color=member.color)
                embed.set_image(url=member.avatar)
                embed.set_footer(
                    icon_url=ctx.author.avatar, text="Imagen pedida por: {}".format(ctx.author))
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("El usuario no tiene avatares para mostrar.")
                
        except Exception as e:
            log.error(str(e))
            return
       
def setup(bot):
    bot.add_cog(General(bot))
