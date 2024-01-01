from datetime import datetime

from scraping.scrape_advancedteamstats import scrape_advanced_all
from scraping.scrape_stats_cli import (
    get_singleseason_stats,
    get_type_key,
    years_valid,
)
from scraping.scrape_teamrecords import scrape_all_team_records
from utils.abbreviate_team_names import add_abbreviated_team_names
from utils.csv_functions import make_dir_if_nonexistent, reset_csv
from utils.vars import curr_season, curr_season_str

short_date = datetime.today().strftime("%Y-%m-%d")
start_date_nodash = short_date.replace("-", "")

directory = "./data/dailystats"
today_dir = f"{directory}/{short_date}"
make_dir_if_nonexistent(today_dir)


def save_each_season_stats_daily(stat_type, year_start, year_end):
    if years_valid(stat_type, year_start, year_end):
        year_list = list(range(int(year_start), int(year_end) + 1))
        type_key = get_type_key(stat_type)

        for year in year_list:
            URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_{type_key}.html"
            filename = f"{today_dir}/{type_key}_{start_date_nodash}.csv"
            reset_csv(filename)
            get_singleseason_stats(year, URL, filename, True)
            print(
                (f"Finished populating season {year - 1}-{year}, {type_key} data."),
            )


def daily_data_script():
    save_each_season_stats_daily("-tot", curr_season_str, curr_season_str)
    save_each_season_stats_daily("-adv", curr_season_str, curr_season_str)
    scrape_all_team_records(
        (f"{today_dir}/teamStandings_{start_date_nodash}.csv"),
        curr_season,
        curr_season,
    )
    add_abbreviated_team_names(
        (f"{today_dir}/teamStandings_{start_date_nodash}.csv"),
    )
    scrape_advanced_all(f"{today_dir}", curr_season_str, curr_season_str)


if __name__ == "__main__":
    daily_data_script()
