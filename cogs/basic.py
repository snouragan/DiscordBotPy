import discord
from discord.ext import commands, tasks
import sys

sys.path.insert(1, './Database/Services')

from dbSetup import DbSetup

class Basic(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  #Event
  @commands.Cog.listener()
  async def on_ready(self):
    print('Bot is online.')
    dbSetup = DbSetup(self.client)
    
  #Command
  @commands.command()
  async def ping(self, ctx):
    await ctx.send('Pong')

  @commands.command()
  async def cap(self, ctx):
    await ctx.send('Iti dau in cap')

  #Background Task
  @tasks.loop(minutes = 2)
  async def salut(self):
    await print('a')


def setup(client):
  client.add_cog(Basic(client))