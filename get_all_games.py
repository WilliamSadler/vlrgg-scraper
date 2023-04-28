import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import csv

TOTAL_PAGES = 375

data_file =  open("all_games.csv", 'w', newline='', encoding="utf8")
write_results = csv.writer(data_file)

header = ["match_date", "team1", "team2", "match_url"]
write_results.writerow(header)

for i in range(1, TOTAL_PAGES):
    print("Page", i)
    url = "https://www.vlr.gg/matches/results/?page=" + str(i)
    print(url)
    page = requests.get(url)

    s = BeautifulSoup(page.content, "html.parser") 

    matches = s.find_all("a", {"class" : "match-item"})

    for m in matches:
        datetime_extracted = m.find_previous("div", {"class" : "wf-label"}).text.strip().split("\t")[0].split("\n")[0]
        datetime_extracted = datetime_extracted.split(" ")

        datetime_string = " ".join(datetime_extracted[1:4])
        datetime_string = re.sub(",", "", datetime_string)

        match_datetime = datetime.strptime(datetime_string, "%B %d %Y")
        match_date = match_datetime.strftime("%d/%m/%Y")

        teams = m.find_all("div", {"class": "text-of"})
        team1 = teams[0].text.strip()
        team2 = teams[1].text.strip()
        
        match_url = m["href"]

        data = [match_date, team1, team2, match_url]
        write_results.writerow(data)