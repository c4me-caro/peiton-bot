import discord
from discord.ext import commands
import math

class Levels(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.levels = {}
    self.xp = {}
    self.max_xp = {}
    
  @discord.slash_command(name="givexp", description="otorga puntos de experiencia a un miembro", guild_ids=['1044359077234479124'])
  @commands.has_any_role('admin supremo', 'staff', 'leader')
  async def give_xp(self, ctx, xp:int, member=None):
    if member == None:
      member = ctx.author
      
    if member.id not in self.levels:
      await ctx.respond("Este usuario no tiene nivel.")
      return
    
    self.xp[member.id] += xp
    if self.xp[member.id] >= self.max_xp[member.id]:
      self.levels[member.id] += round(math.log(self.xp[member.id] / self.max_xp[member.id]))
      self.xp[member.id] = 0
      self.max_xp[member.id] = round(self.max_xp[member.id] * 1.5)
      
      if self.levels[member.id] % 5 == 0:
        await ctx.respond(f'{member.mention} ha subido al nivel {self.levels[member.id]}!')
        return
          
    await ctx.respond(f'{member.mention} ha adquirido {xp} puntos de XP.')

  @discord.slash_command(name="nivel", description="Muestra el nivel actual de un usuario", guild_ids=['1044359077234479124'])
  async def nivel(self, ctx, member: discord.Member = None):
    if member == None:
      member = ctx.author
    
    if member.id not in self.levels:
      await ctx.respond(f'{member.mention} no tiene nivel.')
      return
    
    await ctx.respond(f'{member.mention} tiene el nivel {self.levels[member.id]}. Faltan {self.max_xp[member.id] - self.xp[member.id]} XP para el proximo nivel.')
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    
    if not message.content.startswith(self.bot.command_prefix):
      user = message.author
      
      if user.id not in self.levels:
        self.levels[user.id] = 0
        self.xp[user.id] = 0
        self.max_xp[user.id] = self.bot.initial_max_xp
        await message.channel.send(f'{user.mention} se ha unido a Levels!')

      else:
        self.xp[user.id] += 1 * self.bot.xp_multiplier
        if self.xp[user.id] >= self.max_xp[user.id]:
          self.levels[user.id] += 1
          self.xp[user.id] = 0
          self.max_xp[user.id] = round(self.max_xp[user.id] * 1.5)
          
          if self.levels[user.id] % 5 == 0:
            await message.channel.send(f'{user.mention} ha subido al nivel {self.levels[user.id]}!')
    
def setup(bot):
  bot.add_cog(Levels(bot))