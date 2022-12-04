import requests
from bs4 import BeautifulSoup

from utils.csv_functions import reset_csv
from utils.csv_functions import write_to_csv


fileName = 'baseData/teamStandings.csv'


def scrape_teamrecords(fileName, year):
    yearURL = 'https://www.basketball-reference.com/leagues/NBA_' + \
        str(year) + '.html'
    yearPage = requests.get(yearURL)
    yearSoup = BeautifulSoup(
        yearPage.content, 'html.parser', from_encoding='utf-8',
    )

    teamTable = yearSoup.find('table', id='advanced-team')
    leagueAvg = teamTable.find('tbody').find_all('tr')

    for seasonWL in leagueAvg:
        eachTeam = seasonWL.find_all('td')
        teamWL = []

        for col in eachTeam:
            teamWL.append(col.text)

        teamWL = teamWL[0:1] + teamWL[2:4]

        teamWL.insert(1, year)

        teamWL.append(
            round(int(teamWL[2]) / (int(teamWL[2]) + int(teamWL[3])), 3),
        )
        write_to_csv(fileName, teamWL)
    print(f'Finished populating season {year - 1}-{year}, team standings.')


def scrape_all_team_records(fileName, startYear, endYear):
    yearList = range(int(startYear), int(endYear) + 1)
    reset_csv(fileName)

    write_to_csv(fileName, ['Team', 'Year', 'Wins', 'Losses', 'Perc'])
    for year in yearList:
        scrape_teamrecords(fileName, year)


def main():
    scrape_all_team_records(fileName)


if __name__ == '__main__':
    main()
