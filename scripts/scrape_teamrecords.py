from bs4 import BeautifulSoup
import requests
from csv_functions import write_to_csv
from csv_functions import reset_csv

fileName = 'baseData/teamStandings.csv'

def scrape_teamrecords(fileName, year):
    yearURL = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    yearPage = requests.get(yearURL)
    yearSoup = BeautifulSoup(yearPage.content, 'html.parser', from_encoding = 'utf-8')

    teamTable = yearSoup.find('table', id="advanced-team")
    leagueAvg = teamTable.find('tbody').find_all('tr')

    for seasonWL in leagueAvg:
        eachTeam = seasonWL.find_all('td')
        teamWL = []

        for col in eachTeam:
            teamWL.append(col.text)

        teamWL = teamWL[0:1] + teamWL[2:4]

        teamWL.insert(1, year)

        teamWL.append(round(int(teamWL[2])/(int(teamWL[2])+int(teamWL[3])),3))
        write_to_csv(fileName, teamWL)
        


def scrape_allrecords(fileName):
    yearList = range(1980, 2023)
    reset_csv(fileName)

    write_to_csv(fileName, ['Team', 'Year', 'Wins', 'Losses', 'W/L%'])
    for year in yearList:
        # scrape_teamstats(fileName, year)
        # scrape_teamadvanced(fileName, year)
        scrape_teamrecords(fileName, year)
        

        
def main():
    scrape_allrecords(fileName)


if __name__ == '__main__':
    main()