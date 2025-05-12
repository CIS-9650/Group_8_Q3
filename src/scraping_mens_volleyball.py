# scraping_mens_volleyball.py

# Code for scraping all the names & heghts from all men's volleyball teams. 
# Includes alrernate code in functions for scraping Ball State.
# Creates pandas dataframe, summarizes data, and prints table.

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


def feetToInches(player_height,team):
    
    if team == 'Ball State':
      item = player_height.split("'")
    else:
      item = player_height.split("-")

    feet=int(item[0].strip())
    inches=int(item[1].strip())
    tall = Tallness(feet,inches)
    height_in_inches = tall.inchConvert()
    return height_in_inches

def scrape_page(url):
  page = requests.get(url, headers=headers)
  if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
  else:
    return None

def player_names(soup,team):
  roster_names = []
  if team == 'Ball State':
    names = soup.find_all('h3')
  else:
    names = soup.find_all('td', class_ ='sidearm-table-player-name')
  
  for name in names:
    roster_names.append(name.get_text().strip())
  return roster_names

def player_heights(soup,team):
  roster_heights = []
  if team == 'Ball State':
    heights = soup.find_all('span',class_='s-person-details__bio-stats-item')
    for height in heights:
      if height.get_text().startswith('Height'):
        player_height = height.get_text()[7:-3]
        roster_heights.append(feetToInches(player_height,team))
    return roster_heights
  else:
    heights = soup.find_all('td', class_ ='height')
    for height in heights:
      player_height = height.get_text()
      roster_heights.append(feetToInches(player_height,team))
    return roster_heights

def make_player_dictionary():
  heights = []
  names = []
  for team in volleyball_teams:
    url = volleyball_teams[team]
    soup = scrape_page(url)
    if soup == None:
      continue    
    else:
      heights.extend(player_heights(soup,team))
      names.extend(player_names(soup,team))
  player_dict = {'Name' : names,'Height' : heights}
  return player_dict


def main():
  final = make_player_dictionary()
  df = pd.DataFrame(final)
  print(df.describe())
  print(df)

main()