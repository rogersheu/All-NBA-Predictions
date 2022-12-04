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
mkdir = (f'{directory}/{short_date}')
make_dir_if_nonexistent(mkdir)


def save_each_season_stats_daily(stat_type, year_start, year_end):

    if years_valid(stat_type, year_start, year_end):
        yearList = list(range(int(year_start), int(year_end) + 1))
        typeKey = get_type_key(stat_type)

        for year in yearList:
            URL = (
                f'https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html'
            )
            # f-stringed
            filename = (f'{mkdir}/{typeKey}_{start_date_nodash}.csv')
            reset_csv(filename)
            get_singleseason_stats(year, URL, filename, True)
            # f-stringed
            print(
                (f'Finished populating season {year - 1}-{year}, {typeKey} data.'),
            )
    else:
        return False


def daily_data_script():
    save_each_season_stats_daily('-tot', '2022', '2022')
    save_each_season_stats_daily('-adv', '2022', '2022')
    scrape_all_team_records(
        (f'{mkdir}/teamStandings_{start_date_nodash}.csv'), 2022, 2022,
    )
    add_abbreviated_team_names(
        (f'{mkdir}/teamStandings_{start_date_nodash}.csv'),
    )
    scrape_advanced_all(f'{mkdir}', '1980', '2022')


def main():
    daily_data_script()


if __name__ == '__main__':
    main()
