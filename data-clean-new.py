import csv
import requests
from bs4 import BeautifulSoup
import re

matches = open("world_map_results.csv", 'w', newline='', encoding="utf8")
writer = csv.writer(matches)

import time
start_time = time.time()

with open("all_games.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)
    row_names = ["match_date", "team1", "team2", "score1", "score2", "map_name", "def_start", "match_url"]

    writer.writerow(row_names)

    for entry in reader:
        score1 = -1
        score2 = -1

        match_page_url = "https://www.vlr.gg" + entry["match_url"]
        page = requests.get(match_page_url)

        print(match_page_url)
            
        s = BeautifulSoup(page.content, "html.parser") 

        date_elements = s.find_all("div", {"class": "moment-tz-convert"})
        match_date = date_elements[0]["data-utc-ts"].split(" ")[0]


        maps = s.find_all("div", {"class" : "vm-stats-game-header"})

        for m in maps:
            map_div = m.find("div", {"class" : "map"})
            map_name_unformatted = map_div.find_all("span")[0].text.strip()

            map_name = re.sub(r"[\n\t\s]*", "", map_name_unformatted).split("PICK")[0]

            scores = m.find_all("div", {"class" : "score"})

            score1 = scores[0].text.strip()
            score2 = scores[1].text.strip()

            team1_div = m.find_all("div", {"class" : "team"})[0]
            team1_startside = team1_div.find_all("span")[0]["class"][0]

            if team1_startside == "mod-ct":
                defender_start = 1
            elif team1_startside == "mod-t":
                defender_start = 2
            else:
                defender_start = 0

            data = [match_date, entry["team1"], entry["team2"], score1, score2, map_name, defender_start, entry["match_url"]]

            writer.writerow(data)



print("--- %s seconds ---" % (time.time() - start_time))