# Scraping all season total data from the 1979-1980 season to the
# current season.
import re
import sys
import unicodedata

import requests
from bs4 import BeautifulSoup

from src.utils.csv_functions import make_dir_if_nonexistent
from src.utils.csv_functions import reset_csv
from src.utils.csv_functions import write_to_csv

# tablePattern = re.compile(r"(full_table|italic-text partial-table")

headerExists = False


def get_singleseason_stats(year: str, URL: str, fileName: str, repeatHeader: bool):
    dataPage = requests.get(URL)
    dataSoup = BeautifulSoup(
        dataPage.content, 'html.parser', from_encoding='utf-8',
    )
    dataTable = dataSoup.find('table', class_='sortable')

    # This special i in Omer Asik was the only character in the database not caught by remove_accents.
    turkishCharacters = str.maketrans('ı', 'i')

    if dataTable is not None:
        dataHeader = dataTable.find('thead').find_all('th')
        header = [headerElement.text for headerElement in dataHeader]
        # Removes the initial entries for play-by-play.
        if re.search(r'play-by-play', fileName) is not None:
            header = header[9: len(header)]
        else:
            header = header[1: len(header)]

        header.insert(1, 'PlayerID')
        header.insert(2, 'Year')

        if re.search(r'advanced', fileName):
            header.pop(20)
            header.pop(24)

        if repeatHeader is False:
            global headerExists

            if headerExists is False:
                write_to_csv(fileName, header)
                headerExists = True
        else:
            write_to_csv(fileName, header)

        # Include "italic text" if you want information from players who switched teams.
        dataList = dataTable.find_all('tr', class_=['full_table'])
        # dataList = dataTable.find_all("tr", class_=["full_table", "italic_text"])

        # Pull players who were traded mid-season and just do a check for
        # them later. TBD how to handle their team records. Currently ignoring them, unfortunately.
        # Perhaps a game log search? Having the player code makes it much
        # easier to do a query in the form of
        # basketball-reference.com/players/a/<playerID>/gamelog/<year>

        for player in dataList:
            playerList = player.find_all('td')
            data = [dataItem.text for dataItem in playerList]
            data.insert(1, playerList[0]['data-append-csv'])
            data.insert(2, str(year))
            data[0] = remove_accents(data[0])
            data[0] = data[0].translate(turkishCharacters)
            data[0] = data[0].replace('*', '')
            if re.search(r'advanced', fileName):
                data.pop(20)
                data.pop(24)
            write_to_csv(fileName, data)

    else:
        return False

# Handle weird characters, like Doncic, Zydrunas Ilgauskas, Omer Asik, and more.


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def years_areValid(statType, yearStart, yearEnd):
    if not yearStart.isdigit() or not yearEnd.isdigit():
        print('Please enter integer values.')
        return False

    yearStart = int(yearStart)
    yearEnd = int(yearEnd)

    if (yearStart or yearEnd) < 1947 or (yearStart or yearEnd) > 2022:
        print('Please enter valid years.')
        return False

    if (yearStart or yearEnd) < 1980:
        print('Warning. Picking seasons before the 1979-1980 season will skew data because of the introducton of the 3 point line in 1979.')
        return False

    if yearStart > yearEnd:
        print('Please pick an ending year AFTER your starting year.')
        return False

    if statType == '-pbp' and yearStart < 1997:
        print('Play-by-play data only started in the 1996-1997 season.')
        return False

    else:
        return True


# Goes from 1979-1980 to 2021-2022 (current season)

def save_each_season_stats(statType, yearStart, yearEnd):
    if years_areValid(statType, yearStart, yearEnd):

        yearList = list(range(int(yearStart), int(yearEnd) + 1))

        typeKey = get_typeKey(statType)

        mkdir = (f'baseData/{typeKey}')
        make_dir_if_nonexistent(mkdir)

        for year in yearList:
            URL = (
                f'https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html'
            )
            fileName = (
                f'baseData/{typeKey}/{typeKey}_stats_{year - 1}_{year}.csv'
            )
            reset_csv(fileName)
            get_singleseason_stats(year, URL, fileName, True)
            print(
                f'Finished populating season {year - 1}-{year}, {typeKey} data.',
            )

    else:
        return False


def save_all_stats(statType, yearStart, yearEnd):
    if years_areValid(statType, yearStart, yearEnd):
        yearList = list(range(int(yearStart), int(yearEnd) + 1))

        typeKey = get_typeKey(statType)

        fileName = f'baseData/{typeKey}_allyears.csv'
        reset_csv(fileName)

        for year in yearList:
            URL = (
                f'https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html'
            )
            get_singleseason_stats(year, URL, fileName, False)
            print(
                f'Finished populating season {year-1}-{year}, {typeKey} data.',
            )

    else:
        return True

# REQUIRES PYTHON 3.10, EARLIER VERSIONS CANNOT RUN STRUCTURAL PATTERN MATCHING, LIKE BELOW
# REPLACE WITH IF/ELIF IF NEEDED


def get_typeKey(statType):
    match statType:
        case '-tot':
            typeKey = 'totals'
        case '-adv':
            typeKey = 'advanced'
        case '-pbp':
            typeKey = 'play-by-play'
        case _:
            return False

    return typeKey


# args[0] is -tot/-adv/-pbp
# args[1] is yearStart
# args[2] is yearEnd
# args[3] determines which code to run, YEARLY or ALL
def main():
    args = sys.argv[1:]
    if len(args) == 4:
        if args[3] == 'yearly':
            save_each_season_stats(args[0], args[1], args[2])
        if args[3] == 'all':
            save_all_stats(args[0], args[1], args[2])
    else:
        print('Please enter 4 arguments.')
        return False


if __name__ == '__main__':
    main()
