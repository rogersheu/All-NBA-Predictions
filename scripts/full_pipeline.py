from daily_data_script import daily_data_script
from daily_database_update import daily_database_update
from daily_modeling import automated_modeling
from datetime import date

date_today = date.today()
today = date_today.strftime("%Y-%m-%d")

def full_pipeline():

    daily_data_script()
    daily_database_update()
    automated_modeling(date, date)




def main():
    full_pipeline()

if __name__ == '__main__':
    main()