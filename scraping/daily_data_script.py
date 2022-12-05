from datetime import datetime

from scraping.scrape_advancedteamstats import scrape_advanced_all
from scraping.scrape_stats_cli import get_singleseason_stats
from scraping.scrape_stats_cli import get_type_key
from scraping.scrape_stats_cli import years_valid
from scraping.scrape_teamrecords import scrape_all_team_records
from utils.abbreviate_team_names import add_abbreviated_team_names
from utils.csv_functions import make_dir_if_nonexistent
from utils.csv_functions import reset_csv

short_date = datetime.today().strftime('%Y-%m-%d')
start_date_nodash = short_date.replace('-', '')

directory = './data/dailystats'
today_dir = (f'{directory}/{short_date}')
make_dir_if_nonexistent(today_dir)


def save_each_season_stats_daily(stat_type, year_start, year_end):
    if years_valid(stat_type, year_start, year_end):
        year_list = list(range(int(year_start), int(year_end) + 1))
        type_key = get_type_key(stat_type)

        for year in year_list:
            URL = (
                f'https://www.basketball-reference.com/leagues/NBA_{year}_{type_key}.html'
            )
            filename = (f'{today_dir}/{type_key}_{start_date_nodash}.csv')
            reset_csv(filename)
            get_singleseason_stats(year, URL, filename, True)
            print(
                (f'Finished populating season {year - 1}-{year}, {type_key} data.'),
            )
    else:
        return False


def daily_data_script():
    save_each_season_stats_daily('-tot', '2023', '2023')
    save_each_season_stats_daily('-adv', '2023', '2023')
    scrape_all_team_records(
        (f'{today_dir}/teamStandings_{start_date_nodash}.csv'), 20223, 2023,
    )
    add_abbreviated_team_names(
        (f'{today_dir}/teamStandings_{start_date_nodash}.csv'),
    )
    scrape_advanced_all(f'{today_dir}', '1980', '2023')


if __name__ == '__main__':
    daily_data_script()
