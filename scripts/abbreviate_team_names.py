# Adds abbreviated team names (e.g., Los Angeles Lakers -> LAL) from team_mapping.py to the indicated csv
import team_mapping
import pandas as pd
import collections


def add_abbreviated_team_names():
    df = pd.read_csv('baseData/teamStandings.csv', delimiter=',')

    chainMap = collections.ChainMap(team_mapping.activeTeams, team_mapping.tradedPlayers, team_mapping.defunctTeams)

    tm = [chainMap[df.iloc[row,0]] for row in range(len(df.index))]

    df.insert(1, 'Tm', tm)

    df.to_csv('baseData/teamStandingsAbbrev.csv')

add_abbreviated_team_names()