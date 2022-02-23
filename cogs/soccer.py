import discord
from discord.ext import commands, tasks

class Soccer(commands.Cog):
  def __init__(self, client):
    self.client = client
    #self.test.start()
    
  @tasks.loop(seconds=5.0)
  async def test(self):
    print('a')
    
  @test.before_loop
  async def before_test(self):
    print('waiting...')
    await self.client.wait_until_ready()
    
def setup(client):
  client.add_cog(Soccer(client))