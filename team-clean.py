import csv

common_teams = ['Renegades',
'Sentinels',
'Cloud9',
'Immortals',
'Gen.G',
'TSM',
'Complexity',
'Envy',
'Built By Gamers',
'Soniqs',
'Paper Rex',
'G2 Esports',
'Andbox',
'NRG Esports',
'Knights',
'100 Thieves',
'FaZe Clan'
]

import csv
from collections import Counter

results_BO1_top_teams = open("results_BO1_small.csv", 'w', newline='', encoding="utf8")

write_results = csv.writer(results_BO1_top_teams)

team_names = []
with open("results_BO1.csv", newline='', encoding="utf8") as data:
    reader = csv.DictReader(data)

    row_names = reader.fieldnames
    write_results.writerow(row_names)
    

    for entry in reader:
        team1 = entry["team1"]
        team2 = entry["team2"]

        if (team1 in common_teams) and (team2 in common_teams):
            data = [entry["team1"], entry["team2"], entry["score1"], entry["score2"], entry["time_completed"],
                entry["round_info"], entry["tournament_name"], entry["match_page"]]

            write_results.writerow(data)
