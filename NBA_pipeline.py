from datetime import date

from daily_data_script import daily_data_script
from daily_database_update import database_pipeline
from daily_modeling import automated_modeling

date_today = date.today()
today = date_today.strftime("%Y-%m-%d")

data_path = f"./data/dailystats/{today}"


def daily_pipeline():
    daily_data_script()
    database_pipeline(data_path)
    automated_modeling(today, today)


if __name__ == "__main__":
    daily_pipeline()
