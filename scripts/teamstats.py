from bs4 import BeautifulSoup
import requests
from csv_functions import write_to_csv
from csv_functions import reset_csv


def scrape_teamstats(fileName, year):
    yearURL = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    yearPage = requests.get(yearURL)
    yearSoup = BeautifulSoup(yearPage.content, 'html.parser', from_encoding = 'utf-8')

    teamTable = yearSoup.find('table', id="per_game-team")
    leagueAvg = teamTable.find('tfoot').find_all('td')
    
    averages = []
    for col in leagueAvg:
        averages.append(col.text)
    
    averages.insert(2, year)
    write_to_csv(fileName, averages)





def scrape_allyears():
    yearList = range(1980, 2023)
    fileName = 'baseData/totalteamaverages.csv'
    reset_csv(fileName)
    for year in yearList:
        scrape_teamstats(fileName, year)



scrape_allyears()