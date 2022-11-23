from discord.ext import commands
from bot import utils
from discord import Embed
from config import config
import datetime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say', help='Muestra un mensaje de parte del bot.', aliases=['test', 'echo', 'decir'])
    async def _test(self, ctx, *message: str):
        if not message:
            message = ('Hello', 'World')

        await ctx.send(" ".join(message))

    @commands.command(name='ping', help='Determina la latencia del host remoto.')
    async def _ping(self, ctx, *_):
        await ctx.reply('Pong! {0}'.format(round(self.bot.latency, 1)))

    @commands.command(name='rules', help='Muestra las reglas del servidor', aliases=['reglas', 'ley'])
    async def _rule(self, ctx, *_):
        desire = ''
        with open('config/reglas.txt', 'r') as f:
            desire = f.readlines()
            f.close()

        await utils.message_embed(ctx, "".join(desire))

    @commands.command(name='avatar', help='Muestra el avatar de los usuarios.')
    async def _get_avatar(self, ctx, *_):
        try:
            if not ctx.message.mentions:
                embed = Embed(
                    title='@{}\'s avatar'.format(ctx.author), color=ctx.author.color)
                embed.set_image(url=ctx.author.avatar)
                embed.set_footer(
                    icon_url=ctx.author.avatar, text="Imagen pedida por: {}".format(ctx.author))
                await ctx.send(embed=embed, reference=ctx.message)

            for user in ctx.message.mentions:
                if user.avatar != "":
                    embed = Embed(
                        title='@{}\'s avatar'.format(user.name), color=user.color)
                    embed.set_image(url=user.avatar)
                    embed.set_footer(
                        icon_url=ctx.author.avatar, text="Imagen pedida por: {}".format(ctx.author))
                    await ctx.send(embed=embed, reference=ctx.message)
                else:
                    await utils.alert_embed(ctx, "El usuario {} no tiene avatar".format(user.name))
        except Exception as e:
            print(str(e))
            return

    @commands.command(name='confess', help='Envía una confesión al canal designado. Envialo al DM.', aliases=['confesar', 'confesion'])
    async def _confesar(self, ctx, *texto: str):
        channel = config.confess_channel
        if channel == '':
            await utils.alert_embed(ctx, "El canal de confesiones no ha sido establecido")
            return
            
        channel_obj = self.bot.get_channel(int(channel))
        embed = Embed(title='Confesión anónima',
                      description=" ".join(texto),
                      timestamp=datetime.datetime.utcnow(),
                      color=config.EMBED_COLOR)

        await channel_obj.send(embed=embed)
        print("{} ha confesado: {}".format(ctx.author, texto))
        await ctx.send('Confesión enviada.', reference=ctx.message)


async def setup(bot):
    await bot.add_cog(General(bot))
