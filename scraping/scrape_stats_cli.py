# Scraping all season total data from the 1979-1980 season to the
# current season.
import re
import sys
import unicodedata

import requests
from bs4 import BeautifulSoup

from utils.csv_functions import make_dir_if_nonexistent, reset_csv, write_to_csv
from utils.vars import curr_season

header_exists = False


def get_singleseason_stats(year: str, url: str, filename: str, repeat_header: bool):
    data_page = requests.get(url)
    data_soup = BeautifulSoup(
        data_page.content,
        "html.parser",
        from_encoding="utf-8",
    )
    data_table = data_soup.find("table", class_="sortable")

    # This special i in Omer Asik was the only character in the database not caught by remove_accents.
    turkish_chars = str.maketrans("ı", "i")

    if data_table is not None:
        data_header = data_table.find("thead").find_all("th")
        header = [header_element.text for header_element in data_header]
        # Removes the initial entries for play-by-play.
        if re.search(r"play-by-play", filename) is not None:
            header = header[9 : len(header)]
        else:
            header = header[1 : len(header)]

        header.insert(1, "PlayerID")
        header.insert(2, "Year")

        if re.search(r"advanced", filename):
            header.pop(20)
            header.pop(24)

        if repeat_header is False:
            global header_exists

            if header_exists is False:
                write_to_csv(filename, header)
                header_exists = True
        else:
            write_to_csv(filename, header)

        # Include "italic text" if you want information from players who switched teams.
        data_list = data_table.find_all("tr", class_=["full_table"])
        # dataList = dataTable.find_all("tr", class_=["full_table", "italic_text"])

        # Pull players who were traded mid-season and just do a check for
        # them later. TBD how to handle their team records. Currently ignoring them, unfortunately.
        # Perhaps a game log search? Having the player code makes it much
        # easier to do a query in the form of
        # basketball-reference.com/players/a/<playerID>/gamelog/<year>

        for player in data_list:
            playerList = player.find_all("td")
            data = [dataItem.text for dataItem in playerList]
            data.insert(1, playerList[0]["data-append-csv"])
            data.insert(2, str(year))
            data[0] = remove_accents(data[0])
            data[0] = data[0].translate(turkish_chars)
            data[0] = data[0].replace("*", "")
            if re.search(r"advanced", filename):
                data.pop(20)
                data.pop(24)
            write_to_csv(filename, data)


def remove_accents(input_str):
    # Handle weird characters, like Doncic, Zydrunas Ilgauskas, Omer Asik, and more.
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def years_valid(stat_type, year_start, year_end):
    if not year_start.isdigit() or not year_end.isdigit():
        print("Please enter integer values.")
        return False

    year_start = int(year_start)
    year_end = int(year_end)

    if (year_start or year_end) < 1947 or (year_start or year_end) > curr_season:
        print("Please enter valid years.")
        return False

    if (year_start or year_end) < 1980:
        print(
            "Warning. Picking seasons before the 1979-1980 season will skew data because of the introducton of the 3 point line in 1979."
        )
        return False

    if year_start > year_end:
        print("Please pick an ending year AFTER your starting year.")
        return False

    if stat_type == "-pbp" and year_start < 1997:
        print("Play-by-play data only started in the 1996-1997 season.")
        return False

    return True


def save_each_season_stats(stat_type, year_start, year_end):
    if years_valid(stat_type, year_start, year_end):
        yearList = list(range(int(year_start), int(year_end) + 1))

        typeKey = get_type_key(stat_type)

        mkdir = f"baseData/{typeKey}"
        make_dir_if_nonexistent(mkdir)

        for year in yearList:
            URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html"
            fileName = f"./data/{typeKey}/{typeKey}_stats_{year - 1}_{year}.csv"
            reset_csv(fileName)
            get_singleseason_stats(year, URL, fileName, True)
            print(
                f"Finished populating season {year - 1}-{year}, {typeKey} data.",
            )


def save_all_stats(stat_type, year_start, year_end):
    if years_valid(stat_type, year_start, year_end):
        year_list = list(range(int(year_start), int(year_end) + 1))

        typeKey = get_type_key(stat_type)

        fileName = f"./data/{typeKey}_allyears.csv"
        reset_csv(fileName)

        for year in year_list:
            URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html"
            get_singleseason_stats(year, URL, fileName, False)
            print(
                f"Finished populating season {year-1}-{year}, {typeKey} data.",
            )


# NOTE: REQUIRES PYTHON 3.10
# REPLACE WITH IF/ELIF IF NEEDED
def get_type_key(stat_type):
    match stat_type:
        case "-tot":
            type_key = "totals"
        case "-adv":
            type_key = "advanced"
        case "-pbp":
            type_key = "play-by-play"
        case _:
            type_key = ""

    return type_key


# args[0] is -tot/-adv/-pbp
# args[1] is year_start
# args[2] is year_end
# args[3] determines which code to run, YEARLY or ALL
def stat_scraper():
    args = sys.argv[1:]
    if len(args) == 4:
        if args[3] == "yearly":
            save_each_season_stats(args[0], args[1], args[2])
        if args[3] == "all":
            save_all_stats(args[0], args[1], args[2])
    else:
        print("Please enter 4 arguments.")


if __name__ == "__main__":
    stat_scraper()
