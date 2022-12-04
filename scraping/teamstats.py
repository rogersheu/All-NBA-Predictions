import requests
from bs4 import BeautifulSoup

from utils.csv_functions import reset_csv
from utils.csv_functions import write_to_csv
from utils.transfer_data import pick_path


headerCheck = False


def scrape_teamstats(fileName, year):
    yearURL = (f'https://www.basketball-reference.com/leagues/NBA_{year}.html')
    yearPage = requests.get(yearURL)
    yearSoup = BeautifulSoup(
        yearPage.content, 'html.parser', from_encoding='utf-8',
    )

    teamTable = yearSoup.find('table', id='per_game-team')
    header = []
    headings = teamTable.find('thead').find_all('th')

    for col in headings:
        header.append(col.text)

    global headerCheck
    header = header[1: len(header)]
    header.insert(2, 'Season')
    if headerCheck is False:
        write_to_csv(fileName, header)
        headerCheck = True

    leagueAvg = teamTable.find('tfoot').find_all('td')

    averages = []
    for col in leagueAvg:
        averages.append(col.text)

    averages.insert(1, year)
    write_to_csv(fileName, averages)


def scrape_alltotals(startYear, endYear):
    pathName = pick_path()
    fileName = (f'{pathName}/teamstats.csv')
    yearList = range(int(startYear), int(endYear) + 1)
    reset_csv(fileName)

    for year in yearList:
        scrape_teamstats(fileName, year)
    print('Finished populating {startYear}-{endYear}, team stats.')


def main():
    scrape_alltotals(1980, 2022)


if __name__ == '__main__':
    main()
