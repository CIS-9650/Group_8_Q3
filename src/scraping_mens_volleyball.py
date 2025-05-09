# scraping_mens_volleyball.py

# CODE FOR SCRAPING ALL THE NAMES & HEGHTS FROM ALL MEN'S VOLLEYBALL TEAMS (EXCEPT BALL STATE)
# WITH PANDAS DATAFRAME AND SUMMARY

# this is where the portion of code to scrape the heights of
# the mens' volleyball teams is being developed

import requests
from bs4 import BeautifulSoup
import pandas as pd

volleyball_teams = {
    'City College of New York':'https://ccnyathletics.com/sports/mens-volleyball/roster',
    'Lehman College':'https://lehmanathletics.com/sports/mens-volleyball/roster',
    'Brooklyn College':'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster',
    'John Jay College':'https://johnjayathletics.com/sports/mens-volleyball/roster',
    'Baruch College':'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster',
    'Medgar Evers College':'https://mecathletics.com/sports/mens-volleyball/roster',
    'Hunter College':'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster',
    'York College':'https://yorkathletics.com/sports/mens-volleyball/roster',
    'Ball State':'https://ballstatesports.com/sports/mens-volleyball/roster'
                  }

# headers Source: https://www.zenrows.com/blog/web-scraping-headers#user-agent
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive'
  }

class Tallness:
  
  def __init__(self, feet, inches):
    self.feet = feet
    self.inches = inches

  def __str__(self):
    return f"{self.feet}'{self.inches}"

  def inchConvert(self):
    return self.feet * 12 + self.inches



def feetToInches(player_height):
    item = player_height.split("-")
    feet=int(item[0].strip())
    inches=int(item[1].strip())
    tall = Tallness(feet,inches)
    height_in_inches = tall.inchConvert()
    return height_in_inches


def playerNames_Heights(team,url):

  roster_names = []
  roster_heights = []
  player_dict = {}

  page = requests.get(url, headers=headers)

  if page.status_code == 200:   
    soup = BeautifulSoup(page.content, 'html.parser')
  else:
    return None

  heights = soup.find_all('td', class_ ='height')
  names = soup.find_all('td', class_ ='sidearm-table-player-name')

  for name in names:
    roster_names.append(name.get_text().strip())

  for height in heights:
    h = height.get_text()
    roster_heights.append(feetToInches(h))
  
  for x in range (len(roster_heights)):
    player_dict.update({roster_names[x]:roster_heights[x]})

  return player_dict
    

def makeAllDictionary():
  all_dict = {}

  for team in volleyball_teams:
    url = volleyball_teams[team]
    data = playerNames_Heights(team,url)
    if data == None:
      continue
    all_dict.update(data)
  return all_dict


def main():
  final = makeAllDictionary()
  
  pandas_dict = {
      'Name' : final.keys(),
      'Height' : final.values()
  }

  df = pd.DataFrame(pandas_dict)
  print(df.describe())
  print(df)
  

main()