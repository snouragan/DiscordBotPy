import discord
import os
from log import Log
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
log = Log()
client = commands.Bot(intents = intents, command_prefix = os.getenv('PREFIX') + ' ')

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv('TOKEN')) 

