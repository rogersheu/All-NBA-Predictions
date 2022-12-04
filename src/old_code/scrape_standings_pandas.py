from __future__ import annotations

import pandas as pd
import requests
from csv_functions import reset_csv


def get_standings():
    yearList = range(2021, 2022)
    fileName = 'baseData/teamStandings.csv'
    reset_csv(fileName)

    # write_to_csv(fileName, ['Team', 'Wins','Losses','WL%','Season'])

    for year in yearList:
        URL = (
            'https://www.basketball-reference.com/leagues/NBA_'
            + str(year)
            + '_standings.html'
        )

        standingsPage = requests.get(URL)

        df_list = pd.read_html(standingsPage.text)
        df_currEast = df_list[0]
        df_currWest = df_list[1]

        df_currEast = transform_df(df_currEast, 'Eastern Conference', year)
        df_currWest = transform_df(df_currWest, 'Western Conference', year)


# Need to concatenate and save to CSV


def transform_df(df, teamString, year):
    df = df.iloc[:, 0:3]
    df.rename(columns={teamString: 'Team'}, inplace=True)
    df['Team'] = df['Team'].str.replace('*', '')
    df['W/L%'] = df.W / (df.W + df.L)
    df['Season'] = year

    return df


get_standings()
