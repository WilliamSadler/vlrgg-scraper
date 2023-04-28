import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import csv

NA_TEAMS_URL = "https://www.vlr.gg/rankings/north-america"

#get list of na teams from vlr.gg list
page = requests.get(NA_TEAMS_URL)
soup = BeautifulSoup(page.content, "html.parser") 

na_teams = []

subpage_divs = soup.find_all("a", {"class" : "js-btn-collapsible"})

for p in subpage_divs:

    subpage_url = "http://vlr.gg" + p["href"]
    print(subpage_url)

    subpage = requests.get(subpage_url)
    s = BeautifulSoup(subpage.content, "html.parser") 

    team_divs = s.find_all("div", {"class": "ge-text"})

    for t in team_divs:
        na_teams.append(t.text.strip().split("\n")[0][:-1])


na_matches = open("na_games.csv", 'w', newline='', encoding="utf8")
writer = csv.writer(na_matches)

print(na_teams)
input()

with open("all_games.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)
    row_names = reader.fieldnames

    writer.writerow(row_names)

    i = 1

    for entry in reader:
        print("Game", i)
        team1 = entry["team1"]
        team2 = entry["team2"]
        
        if (team1 in na_teams) and (team2 in na_teams):
            print("Local NA Match Found!")
            print(team1)
            print(team2)

            data = [entry["match_date"], team1, team2, entry["match_url"]]
            print(data)

            writer.writerow(data)
        #else:
            #print(team1)
            #print(team2)
            #print("Not a Local NA Match")

        i = i+1