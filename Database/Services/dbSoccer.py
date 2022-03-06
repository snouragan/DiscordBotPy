import sqlite3

class DbSoccer():
  def addBet(user_id, value, match_id, team):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()
    command = f"""INSERT OR IGNORE INTO bets VALUES ({user_id}, {value}, {match_id}, {team});"""
    curs.execute(command)
    connection.commit()
    
    connection.close()

  def addEmbed(message_id, match_id):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()
    command = f"""INSERT OR IGNORE INTO embeds VALUES ({message_id}, {match_id});"""
    curs.execute(command)
    connection.commit()
    
    connection.close()

  def getMatchByMessage(message_id):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()
    command = f"""SELECT match_id FROM embeds WHERE message_id = {message_id};"""
    curs.execute(command)
    match_id = curs.fetchall()
    
    connection.close()
    return match_id