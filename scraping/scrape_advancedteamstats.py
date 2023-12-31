from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils.csv_functions import reset_csv
from utils.csv_functions import write_to_csv


short_date = datetime.today().strftime('%Y-%m-%d')
short_date_nodash = short_date.replace('-', '')

directory = './data/dailystats'
mkdir = (f'{directory}/{short_date}')


def scrape_teamadvanced(filename, year):
    year_url = (
        f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    )
    year_page = requests.get(year_url)
    year_soup = BeautifulSoup(
        year_page.content, 'html.parser', from_encoding='utf-8',
    )

    team_table = year_soup.find('table', id='advanced-team')
    league_avg = team_table.find('tfoot').find_all('td')

    averages = []
    for col in league_avg:
        averages.append(col.text)

    averages = averages[12:16]

    averages.insert(1, year)
    write_to_csv(filename, averages)


def scrape_advanced_all(path_name, start_year, end_year):
    filename = (f'{path_name}/teamadv.csv')
    year_list = range(int(start_year), int(end_year) + 1)
    reset_csv(filename)
    write_to_csv(filename, ['Pace', 'Season', 'FTr', '3PAr', 'TS%'])
    for year in year_list:
        scrape_teamadvanced(filename, year)
    print(f'Finished populating {start_year}-{end_year}, team advanced stats.')
