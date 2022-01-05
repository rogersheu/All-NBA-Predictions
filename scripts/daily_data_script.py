from tkinter.constants import S
from scrape_stats_cli import get_singleseason_stats, get_typeKey, years_areValid
from csv_functions import make_dir_if_nonexistent, reset_csv
from scrape_teamrecords import scrape_all_team_records
from datetime import datetime
from abbreviate_team_names import add_abbreviated_team_names
from scrape_advancedteamstats import scrape_alladvanced

shortDate = datetime.today().strftime('%Y-%m-%d')
shortDate_nodash = shortDate.replace("-","")

directory= "./baseData/dailystats"
mkdir = (f"{directory}/{shortDate}")
make_dir_if_nonexistent(mkdir)

def save_each_season_stats_daily(statType, yearStart, yearEnd):

    if years_areValid(statType, yearStart, yearEnd):
        yearList = list(range(int(yearStart), int(yearEnd) + 1))
        typeKey = get_typeKey(statType)

        for year in yearList:
            URL = (f"https://www.basketball-reference.com/leagues/NBA_{year}_{typeKey}.html")
            fileName = (f"{mkdir}/{typeKey}_{shortDate_nodash}.csv") # f-stringed
            reset_csv(fileName)
            get_singleseason_stats(year, URL, fileName, True)
            print((f"Finished populating season {year - 1}-{year}, {typeKey} data.")) # f-stringed
    else:
        return False


def main():
    save_each_season_stats_daily('-tot', '2022', '2022')
    save_each_season_stats_daily('-adv', '2022', '2022')
    scrape_all_team_records((f"{mkdir}/teamStandings_{shortDate_nodash}.csv"), 2022, 2022)
    add_abbreviated_team_names((f"{mkdir}/teamStandings_{shortDate_nodash}.csv"))
    scrape_alladvanced(f"{mkdir}", '1980', '2022')


if __name__ == '__main__':
    main()