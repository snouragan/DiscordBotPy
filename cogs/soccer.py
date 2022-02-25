import discord
from discord.ext import commands, tasks
from soccer_api import SoccerAPI

class Soccer(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.soccerAPI = SoccerAPI()
    self.soccerAPI.getMatchesScheduledToday()
    self.soccerAPI.getMatchesFinishedToday()
    self.soccerAPI.getTeam(2)
    self.sendScheduledMatchesEmbeds.start()

  @commands.Cog.listener()
  async def on_reaction_add(reaction, user):
    if user != self.client.user:
      print(user)
    
  @tasks.loop(minutes = 10)
  async def sendScheduledMatchesEmbeds(self):
    # for emoji in self.client.emojis:
    #     print("Name:", emoji.name + ",", "ID:", emoji.id)
    embeds = self.createScheduledMatchesEmbeds()
    for embed in embeds:
      msg = await self.client.get_guild(657569969839800320).get_channel(814964956557738035).send(embed=embed)
      await msg.add_reaction(self.client.get_emoji(':rl_bronze:817330551521411072'))
      await msg.add_reaction(self.client.get_emoji(':rl_silver:817329105761468456'))
      await msg.add_reaction(self.client.get_emoji(':rl_gold:817328784348545035'))
      
  @sendScheduledMatchesEmbeds.before_loop
  async def before_test(self):
    print('waiting...')
    await self.client.wait_until_ready()

  def createScheduledMatchesEmbeds(self):
    matches = self.soccerAPI.getMatchesScheduledToday()
    count = matches["count"]
    match_embeds = []
    for i in range(count):
      home_team_name = matches["matches"][i]["homeTeam"]["name"]
      away_team_name = matches["matches"][i]["awayTeam"]["name"]
      
      home_team_id = matches["matches"][i]["homeTeam"]["id"]
      away_team_id = matches["matches"][i]["awayTeam"]["id"]

      home_team_crestUrl = self.soccerAPI.getTeam(home_team_id)["crestUrl"]
      away_team_crestUrl = self.soccerAPI.getTeam(away_team_id)["crestUrl"]
      
      embed = discord.Embed(title='Upcoming Match', description=f'{home_team_name} vs {away_team_name}')
      embed.set_image(url = home_team_crestUrl)
      embed.set_thumbnail(url = away_team_crestUrl)
      
      match_embeds.append(embed)

    return match_embeds
  
def setup(client):
  client.add_cog(Soccer(client))