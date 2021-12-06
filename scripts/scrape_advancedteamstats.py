from bs4 import BeautifulSoup
import requests
from csv_functions import *
from transfer_data import *



def scrape_teamadvanced(fileName, year):
    yearURL = (f'https://www.basketball-reference.com/leagues/NBA_{year}.html')
    yearPage = requests.get(yearURL)
    yearSoup = BeautifulSoup(yearPage.content, 'html.parser', from_encoding = 'utf-8')

    teamTable = yearSoup.find('table', id="advanced-team")
    leagueAvg = teamTable.find('tfoot').find_all('td')
    

    averages = []
    for col in leagueAvg:
        averages.append(col.text)
    
    averages = averages[12:16]

    averages.insert(1, year)
    write_to_csv(fileName, averages)



def scrape_alladvanced(pathName, startYear, endYear):
    # pathName = pick_path()
    fileName = (f"{pathName}/teamadv.csv")
    yearList = range(int(startYear), int(endYear) + 1)
    reset_csv(fileName)
    write_to_csv(fileName, ['Pace', 'Season', 'FTr', '3PAr', 'TS%'])
    for year in yearList:
        scrape_teamadvanced(fileName, year)
    print(f"Finished populating {startYear}-{endYear}, team advanced stats.")


def main():
    scrape_alladvanced(1980, 2022)


if __name__ == '__main__':
    main()