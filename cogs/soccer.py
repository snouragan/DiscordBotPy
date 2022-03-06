import discord
from discord.ext import commands, tasks
from soccer_api import SoccerAPI
import sys
sys.path.insert(1, './Database/Services')
from dbSoccer import DbSoccer 
import time
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import requests

emojiX = 948495740186005564
emoji2 = 948495739951144991
emoji1 = 948495740072767538

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)

class Soccer(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.soccerAPI = SoccerAPI()
    self.soccerAPI.getMatchesScheduledToday()
    self.soccerAPI.getMatchesFinishedToday()
    self.soccerAPI.getTeam(2)
    self.sendScheduledMatchesEmbeds.start()
  
  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    print('a')
    if user != self.client.user:
      message_id = reaction.message.id
      if reaction == self.client.get_emoji(emoji1):
        team = 'home_team'
        DbSoccer.addBet(user.id, 500, DbSoccer.getMatchByMessage(message_id), team)
      
      elif reaction == self.client.get_emoji(emojiX):
        team = 'draw'
        DbSoccer.addBet(user.id, 500, "match_id", team)
    
      elif reaction == self.client.get_emoji(emoji2):
        team = 'away_team'
        DbSoccer.addBet(user.id, 500, "match_id", team)
    
  @tasks.loop(minutes = 5)
  async def sendScheduledMatchesEmbeds(self):
    embeds, match_ids = self.createScheduledMatchesEmbeds()
    for embed, match_id in zip(embeds, match_ids):
      msg = await self.client.get_guild(657569969839800320).get_channel(814964956557738035).send(embed=embed)
      await msg.add_reaction(self.client.get_emoji(emoji1))
      await msg.add_reaction(self.client.get_emoji(emojiX))
      await msg.add_reaction(self.client.get_emoji(emoji2))
      DbSoccer.addEmbed(msg.id, match_id)
      
  @sendScheduledMatchesEmbeds.before_loop
  async def before_test(self):
    print('waiting...')
    await self.client.wait_until_ready()

  def createScheduledMatchesEmbeds(self):
    matches = self.soccerAPI.getMatchesScheduledToday()
    count = matches["count"]
    match_ids = []
    match_embeds = []
    for i in range(count):
      home_team_name = matches["matches"][i]["homeTeam"]["name"]
      away_team_name = matches["matches"][i]["awayTeam"]["name"]
      
      home_team_id = matches["matches"][i]["homeTeam"]["id"]
      away_team_id = matches["matches"][i]["awayTeam"]["id"]

      home_team_crestUrl = self.soccerAPI.getTeam(home_team_id)["crestUrl"]
      if home_team_crestUrl.endswith('.svg'):
        open('PNG/home_team_crest.png', 'wb').write(requests.get(home_team_crestUrl).content)
        print('png downloaded')
        home_team_crestUrl = './PNG/home_team_crest.png'
        
      away_team_crestUrl = self.soccerAPI.getTeam(away_team_id)["crestUrl"]
      if away_team_crestUrl.endswith('.svg'):
        open('PNG/away_team_crest.png', 'wb').write(requests.get(home_team_crestUrl).content)
        print('png downloaded')
        away_team_crestUrl = './PNG/away_team_crest.png'
        
      embed = discord.Embed(title='Upcoming Match', description=f'{home_team_name} vs {away_team_name}')
      file = discord.File(home_team_crestUrl, filename="home_team_crest.png")
      embed.set_image(url = "attachment://image.png")
      file = discord.File(home_team_crestUrl, filename="away_team_crest.png")
      embed.set_thumbnail(url = "attachment://image.png")
      
      match_embeds.append(embed)
      match_ids.append(matches["matches"][i]["id"])
      time.sleep(30)

    return match_embeds, match_ids
  
def setup(client):
  client.add_cog(Soccer(client))