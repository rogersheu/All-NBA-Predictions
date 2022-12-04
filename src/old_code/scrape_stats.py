# Scraping all season total data from the 1979-1980 season to the
# current season.
from __future__ import annotations

import os
import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from csv_functions import reset_csv
from csv_functions import write_to_csv

# tablePattern = re.compile(r"(full_table|italic-text partial-table")

headerExists = False


def get_singleseason_stats(year, URL, fileName):
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

        global headerExists

        if headerExists is False:
            write_to_csv(fileName, header)
            headerExists = True

        # Include "italic text" if you want information from players who switched teams.
        dataList = dataTable.find_all('tr', class_=['full_table'])
        # dataList = dataTable.find_all("tr", class_=["full_table", "italic_text"])

        # Pull players who got changed teams mid-season and just do a check for
        # them later. TBD how to handle their team records.
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
            write_to_csv(fileName, data)

    else:
        return False

# Handle weird characters, like Doncic, Zydrunas Ilgauskas, Omer Asik, and more.


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


# Goes from 1979-1980 to 2021-2022 (current season)
def get_each_season_totals():
    print('Do you want (A) Total Stats, (B) Advanced Stats, or (C) Play-by-Play Stats?')
    statType = input('A, B, or C?  ')

    # Account for User Error
    if statType not in ['A', 'B', 'C']:
        print('Please enter a valid letter.')

    print('Please provide the first year for which you want data.')
    print('For a single season, enter the same number for both.')
    print('Example 1: Entering 2020 and 2020 gives the 2019-2020 season.')
    print('Example 2: Entering 1980 and 2022 gives seasons 1979-1980 through 2021-2022.')
    yearStart = input('Starting Year:  ')

    yearEnd = input(
        "Please provide the last year's worth of data you would like. \nEnding Year:  ",
    )

    # Limiting user inputs to valid options.
    # Checks for numeric inputs, followed by valid years.
    # Could probably be try/except blocked, but these if statements do the trick for now.
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

    if statType == 'C' and yearStart < 1997:
        print('Play-by-play data only started in the 1996-1997 season.')
        return False

    else:
        # Added [] around range to save a line.
        yearList = list(range(yearStart, yearEnd + 1))

        if statType == 'A':
            typeKey = 'totals'

        elif statType == 'B':
            typeKey = 'advanced'

        elif statType == 'C':
            typeKey = 'play-by-play'

        # Use this portion to save it all into one file.

        # fileName = f"baseData/{typeKey}_allyears.csv" # f-stringed
        # reset_csv(fileName)

        # for year in yearList:
        #     URL = (f"https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html") # f-stringed
        #     get_singleseason_stats(year, URL, fileName)
        #     print(f"Finished populating season {year-1}-{year}.") # Changed to f-string.

        ###########################################################################################################

        # Use this portion to save all into separate files.

        mkdir = 'baseData/' + typeKey
        if not os.path.exists(mkdir):
            os.makedirs(mkdir)

        for year in yearList:
            URL = (
                f'https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html'
            )
            # f-stringed
            fileName = (
                f'baseData/{typeKey}/{typeKey}_stats_{year - 1}_{year}.csv'
            )

            reset_csv(fileName)

            get_singleseason_stats(year, URL, fileName)
            # f-stringed
            print(f'Finished populating season {year - 1}-{year}.')


def main():
    get_each_season_totals()


if __name__ == '__main__':
    main()
