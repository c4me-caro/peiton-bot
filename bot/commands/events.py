from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from discord.utils import get
from discord.ext import commands
from bot.logs import Logger

log = Logger("commands.log", 3)

class Events(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.log("Bot Online!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        log.error("Bot was disconnected")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions and not message.content.startswith(self.bot.command_prefix):
            await message.channel.send("Hola, necesitas algo? Puedes usar `" + self.bot.command_prefix + "help` para obtener ayuda ^^")
            return

def setup(bot):
    bot.add_cog(Events(bot))
