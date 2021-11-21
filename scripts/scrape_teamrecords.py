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
    leagueAvg = teamTable.find('tfoot').find_all('td')
    

    averages = []
    for col in leagueAvg:
        averages.append(col.text)
    
    averages = averages[0:1] + averages[2:4]

    averages.insert(1, year)

    averages.insert(5, round(averages[3]/(averages[3]+averages[4]),3))
    write_to_csv(fileName, averages)
    


def scrape_allrecords(fileName):
    yearList = range(1980, 2023)
    reset_csv(fileName)

    write_to_csv(fileName, ['Team', 'Year', 'Wins', 'Losses'])
    for year in yearList:
        # scrape_teamstats(fileName, year)
        # scrape_teamadvanced(fileName, year)
        scrape_teamrecords(fileName, year)
        

scrape_allrecords(fileName)