import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def import_playerIDs():

    df = pd.read_csv('./baseData/dailystats/2021-12-22/totals_20211222.csv')

    playerIDs = df['PlayerID']

    bdays, ages = map(list, zip(*[get_bdays(id) for id in playerIDs]))

    df.insert(2, 'Birth Date', bdays)
    df['Age'] = ages

    df.to_csv('./baseData/player_birthdates_2022.csv')


def get_bdays(playerID):
    initial = playerID[0]
    playerURL = f'https://www.basketball-reference.com/players/{initial}/{playerID}.html'
    time.sleep(1.0 / 250)
    playerPage = requests.get(playerURL)
    playerSoup = BeautifulSoup(
        playerPage.content, 'html.parser', from_encoding='utf-8',
    )
    playerBday = playerSoup.find('span', id='necro-birth')['data-birth']
    playerBday = datetime.datetime.strptime(playerBday, '%Y-%m-%d')
    today = datetime.datetime.now()

    age = (today - playerBday).days
    age = round(age / 365.25, 1)  # Approximates age

    playerBday = playerBday.date()
    print(f'{playerID} | {playerBday} | {age}')
    return playerBday, age


if __name__ == '__main__':
    import_playerIDs()
