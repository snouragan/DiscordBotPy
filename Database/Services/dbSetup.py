import sqlite3
import discord
from discord.ext import commands

class DbSetup:
  def __init__(self, client):
    self.client = client
    self.createTable()

  def createTable(self):

    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    command = """CREATE TABLE if NOT EXISTS members ( 
      id UNSIGNED BIG INT NOT NULL PRIMARY KEY UNIQUE,
      credit INT DEFAULT 0);"""
    curs.execute(command)
    connection.commit()
    connection.close()
    self.populateMembersTable()

  def populateMembersTable(self):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()
    for guild in self.client.guilds:
        for member in guild.members:
            command = f"""INSERT OR IGNORE INTO members VALUES ({member.id}, 0);"""
            curs.execute(command)
            connection.commit()
    
    connection.close()