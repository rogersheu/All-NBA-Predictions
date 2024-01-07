import requests
from bs4 import BeautifulSoup

from utils.csv_functions import reset_csv
from utils.csv_functions import write_to_csv


team_standings_fname = "data/teamStandings.csv"


def scrape_teamrecords(filename, year):
    year_url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
    year_page = requests.get(year_url)
    year_soup = BeautifulSoup(
        year_page.content,
        "html.parser",
        from_encoding="utf-8",
    )

    team_table = year_soup.find("table", id="advanced-team")
    league_avg = team_table.find("tbody").find_all("tr")

    for season_wl in league_avg:
        each_team = season_wl.find_all("td")
        team_wl = []

        for col in each_team:
            team_wl.append(col.text)

        team_wl = team_wl[0:1] + team_wl[2:4]

        team_wl.insert(1, year)

        team_wl.append(
            round(int(team_wl[2]) / (int(team_wl[2]) + int(team_wl[3])), 3),
        )
        write_to_csv(filename, team_wl)
    print(f"Finished populating season {year - 1}-{year}, team standings.")


def scrape_all_team_records(filename, start_year, end_year):
    year_list = range(int(start_year), int(end_year) + 1)
    reset_csv(filename)

    write_to_csv(filename, ["Team", "Year", "Wins", "Losses", "Perc"])
    for year in year_list:
        scrape_teamrecords(filename, year)


if __name__ == "__main__":
    scrape_all_team_records()
