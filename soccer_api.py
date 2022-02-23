import http.client
import json
from datetime import date, timedelta

class SoccerAPI:
  def getMatchesFinished(self):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '200c3cdb3bd348aa89a5f82018066554' }
    connection.request('GET', f'/v2/competitions/PL/matches?dateFrom={self.getDateYesterday()}&dateTo={self.getDateToday()}&status=FINISHED', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    with open('finished_matches.json', 'w') as outfile:
      json.dump(response, outfile)
    print('finished matches')
    
  def getMatchesScheduledToday(self):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '200c3cdb3bd348aa89a5f82018066554' }
    connection.request('GET', f'/v2/competitions/PL/matches?dateFrom={self.getDateToday()}&dateTo={self.getDateTomorrow()}&status=SCHEDULED', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    with open('scheduled_matches.json', 'w') as outfile:
      json.dump(response, outfile)
    print('scheduled matches')
    
  def getDateToday(self):
    todayDate = date.today().strftime("%d/%m/%Y").split('/') 
    today = todayDate[2] + '-' + todayDate[1] + '-' + todayDate[0]
    print(today)
    return today
    
  def getDateTomorrow(self):
    tomorrowDate = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y").split('/') 
    tomorrow = tomorrowDate[2] + '-' + tomorrowDate[1] + '-' + tomorrowDate[0]
    return tomorrow
    
  def getDateYesterday(self):
    yesterdayDate = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y").split('/') 
    yesterday = yesterdayDate[2] + '-' + yesterdayDate[1] + '-' + yesterdayDate[0]
    return yesterday