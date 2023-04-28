import csv
import requests
from bs4 import BeautifulSoup
import re

matches = open("na_map_results_players.csv", 'w', newline='', encoding="utf8")
writer = csv.writer(matches)

completed_games = ["all"]

import time
start_time = time.time()

with open("na_games_common.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)
    row_names = ["match_date", "team1", "team2", "score1", "score2", "map_name", "def_start", 
    "t1p1", "t1p2","t1p3","t1p4","t1p5","t2p1","t2p2","t2p3","t2p4","t2p5", 
    "match_url"]

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


        maps = s.find_all("div", {"class" : "vm-stats-game"})
        print(len(maps))
        for m2 in maps:
            game_id = m2["data-game-id"]
            if(not(game_id in completed_games)):
                #m = s.find("div", {"class" : "vm-stats-game-header"})
                map_div = m2.find("div", {"class" : "map"})
                map_name_unformatted = map_div.find_all("span")[0].text.strip()

                map_name = re.sub(r"[\n\t\s]*", "", map_name_unformatted).split("PICK")[0]

                scores = m2.find_all("div", {"class" : "score"})

                players = m2.find_all("a")

                player_ids = []
                for p in players:
                    player_ids.append(p["href"].split("/player/")[1].split("/")[0])
                
                t1p1 = -1
                t1p2 = -1
                t1p3 = -1
                t1p4 = -1
                t1p5 = -1
                t2p1 = -1
                t2p2 = -1
                t2p3 = -1
                t2p4 = -1
                t2p5 = -1

                try:
                    t1p1 = player_ids[0]
                    t1p2 = player_ids[1]
                    t1p3 = player_ids[2]
                    t1p4 = player_ids[3]
                    t1p5 = player_ids[4]

                    t2p1 = player_ids[5]
                    t2p2 = player_ids[6]
                    t2p3 = player_ids[7]
                    t2p4 = player_ids[8]
                    t2p5 = player_ids[9]
                except:
                    print("Failed to load players")

                score1 = scores[0].text.strip()
                score2 = scores[1].text.strip()

                team1_div = m2.find_all("div", {"class" : "team"})[0]
                team1_startside = team1_div.find_all("span")[0]["class"][0]

                if team1_startside == "mod-ct":
                    defender_start = 1
                elif team1_startside == "mod-t":
                    defender_start = 2
                else:
                    defender_start = 0

                data = [match_date, entry["team1"], entry["team2"], score1, score2, map_name, defender_start, 
                                t1p1, t1p2, t1p3, t1p4, t1p5, t2p1, t2p2, t2p3, t2p4, t2p5, entry["match_url"]]

                print(scores)
                print(data)

                completed_games.append(game_id)
                #input()
                writer.writerow(data)



print("--- %s seconds ---" % (time.time() - start_time))