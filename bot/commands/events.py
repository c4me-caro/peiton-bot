from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from discord.utils import get
from bot import utils
from config import config
from discord.ext import commands


class Events(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("bot online!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print("bot was disconected.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await utils.not_found_embed(ctx)
            return

        if isinstance(error, MissingRequiredArgument):
            await utils.alert_embed(ctx, "No has ingresado un argumento necesario.")
            return

        if isinstance(error, ZeroDivisionError):
            await utils.alert_embed(ctx, "Has creado una división prohibida por cero.")
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions and not message.content.startswith(config.bot_prefix):
            await utils.message_embed(message.channel, "Hola, necesitas algo? Usa el prefijo \"" + config.bot_prefix + "\" ^^")
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        for msg_id in config.autorol_messages:
            if payload.message_id != int(msg_id) or not payload.emoji.name in config.autorol_corespondence.keys():
                continue

            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = get(
                guild.roles, name=config.autorol_corespondence[payload.emoji.name])

            if role == None or member == None:
                print("Ha ocurrido un error con los roles.")
                continue

            await member.add_roles(role)
            print("rol {} añadido al usuario {}".format(role, member))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member.bot:
            return

        for msg_id in config.autorol_messages:
            if payload.message_id != int(msg_id) or not payload.emoji.name in config.autorol_corespondence.keys():
                continue

            role = get(
                guild.roles, name=config.autorol_corespondence[payload.emoji.name])
            if role == None:
                print("Ha ocurrido un error con los roles.")
                continue

            await member.remove_roles(role)
            print("rol {} removido del usuario {}".format(role, member))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(config.general_channel)
        guild = member.guild

        for i in config.on_join_roles:
            role = get(guild.roles, name=i)
            if role == None:
                print("Ha ocurrido un error con los roles.")
                continue

            await member.add_roles(role)

        print("{} se ha unido al servidor {} con los roles {}".format(
            member, member.guild, config.on_join_roles))
        channel.send("Bienvenid@, {}".format(member.name))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print('Member {} has leaved the guild'.format(member))


async def setup(bot):
    await bot.add_cog(Events(bot))
