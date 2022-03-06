import sqlite3

class DbCredit():
  def getMemberCredit(self, id):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    command = f"""SELECT credit FROM members WHERE id = {id}"""

    curs.execute(command)
    credit = curs.fetchall()
    connection.close()

    return credit[0][0]
  
  def setMemberCredit(self, id, credit):
    connection = sqlite3.connect("database.db")
    curs = connection.cursor()

    command = f"""UPDATE members SET credit = {credit} WHERE id = {id}"""
    
    curs.execute(command)
    connection.commit()
    connection.close()

  def increaseMemberCredit(self, id, credit):
    self.setMemberCredit(id, self.getMemberCredit(id) + credit)
