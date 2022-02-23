from discord.ext import commands, tasks
import sys
sys.path.insert(1, './Database/Services')
from dbSocialCredit import DbSocialCredit

class SocialCredit(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.db = DbSocialCredit()

  @commands.command()
  async def credit(self, ctx):
    id = ctx.message.author.id
    credit = self.db.getMemberCredit(id)
    await ctx.send(credit)

  @commands.Cog.listener()
  async def on_message(self, message):
    id = message.author.id
    credit = self.db.getMemberCredit(id)
    credit += 1
    self.db.setMemberCredit(id, credit)
  

def setup(client):
  client.add_cog(SocialCredit(client))