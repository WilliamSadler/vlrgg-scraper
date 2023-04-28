import csv
from collections import Counter

NUM_TEAMS = 32

team_names = []
with open("na_map_results_players.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)

    row_names = reader.fieldnames
    

    for entry in reader:
        team_names.append(entry["team1"])
        team_names.append(entry["team2"])

c=Counter(team_names)
common = c.most_common(NUM_TEAMS)

common_teams = []

for t in common:
    print(t[0])
    common_teams.append(t[0])

print(common_teams)

results_BO1_top_teams = open("na_games_common_players.csv", 'w', newline='', encoding="utf8")
writer = csv.writer(results_BO1_top_teams)

team_names = []
with open("na_map_results_players.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)

    row_names = reader.fieldnames
    writer.writerow(row_names)
    

    for entry in reader:
        team1 = entry["team1"]
        team2 = entry["team2"]

        if (team1 in common_teams) and (team2 in common_teams):
            data = [entry["match_date"], entry["team1"], entry["team2"], entry["score1"], entry["score2"],
                entry["map_name"], entry["def_start"], 
                entry["t1p1"], entry["t1p2"], entry["t1p3"], entry["t1p4"], entry["t1p5"], entry["t2p1"], entry["t2p2"], entry["t2p3"], entry["t2p4"], entry["t2p5"]
                , entry["match_url"]]

            writer.writerow(data)
