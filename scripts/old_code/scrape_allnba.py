# Deprecated by pulling a data frame using nbastatR in R.
from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from csv_functions import reset_csv
from csv_functions import write_to_csv

fileName = 'baseData/allNBA.csv'


def scrape_allnbateam(fileName, year):
    seasonPage = requests.get(
        f'https://www.basketball-reference.com/leagues/NBA_{year}.html',
    )
    seasonSoup = BeautifulSoup(
        seasonPage.content, 'html.parser', from_encoding='utf-8',
    )

    allNBATable = seasonSoup.find('div', id='all_all-nba')

    for comments in allNBATable.findAll(text=lambda text: isinstance(text, Comment)):
        commentSoup = comments.extract()
        break

    allNBAPlayers = []
    # for player in allNBAList:
    #     if player is None:
    #         continue
    #     else:
    #         allNBAPlayers.append(player.text)

    # write_to_csv(fileName, allNBAPlayers)


def scrape_allseasons(fileName):
    yearList = range(2020, 2021)
    reset_csv(fileName)

    for year in yearList:
        scrape_allnbateam(fileName, year)


scrape_allseasons(fileName)
