import sqlite3

class DbSetup:
  def __init__(self, client):
    self.client = client
    self.createMembersTable()
    self.createBetsTable()
    self.createEmbedsTable()

  def createMembersTable(self):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    command = """CREATE TABLE if NOT EXISTS members ( 
      id UNSIGNED BIG INT NOT NULL PRIMARY KEY UNIQUE,
      credit INT DEFAULT 0);"""
    curs.execute(command)
    connection.commit()
    connection.close()
    self.populateMembersTable()

  def createEmbedsTable(self):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    command = """CREATE TABLE if NOT EXISTS embeds ( 
      message_id UNSIGNED BIG INT NOT NULL,
      match_id UNSIGNED BIG INT NOT NULL);"""
    curs.execute(command)
    connection.commit()
    connection.close()

  def createBetsTable(self):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    # team: home_team / away_team
    command = """CREATE TABLE if NOT EXISTS bets ( 
      user_id UNSIGNED BIG INT NOT NULL,
      value INT DEFAULT 500,
      match_id UNSIGNED BIG INT NOT NULL,
      team VARCHAR
      );"""
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
