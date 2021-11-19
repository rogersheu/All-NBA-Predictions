from bs4 import BeautifulSoup, Comment
import requests
from csv_functions import write_to_csv
from csv_functions import reset_csv



def get_team_standings():
    yearList = range(1980, 2022)
    fileName = "baseData/teamStandings.csv"
    reset_csv(fileName)

    write_to_csv(fileName, ['Team', 'Wins','Losses','WL%','Season'])

    for year in yearList:
        URL = (
            "https://www.basketball-reference.com/leagues/NBA_"
            + str(year)
            + "_standings.html"
        )

        standingsPage = requests.get(URL)
        standingsSoup = BeautifulSoup(standingsPage.content, "html.parser", from_encoding="utf-8")
        # standingsTable = standingsSoup.find('div', id="expanded_standings_sh")

        for team in teamList:
            dataList = team.find_all('td')
            print(dataList)
            teamName = dataList[0].text
            teamRecord = dataList[1].text
            wl = teamRecord.split('-')
            wins = int(wl[0])
            losses = int(wl[1])
            wl_perc = wins / (wins + losses)
            write_to_csv(fileName, [teamName, wl[0], wl[1], wl_perc, year])



get_team_standings()