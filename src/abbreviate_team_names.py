# Adds abbreviated team names (e.g., Los Angeles Lakers -> LAL) from team_mapping.py to the indicated csv
from __future__ import annotations

import collections

import pandas as pd
import team_mapping

fileName = 'baseData/teamStandings.csv'


def add_abbreviated_team_names(fileName):
    df = pd.read_csv(fileName, delimiter=',')

    chainMap = collections.ChainMap(
        team_mapping.activeTeams, team_mapping.tradedPlayers, team_mapping.defunctTeams,
    )

    tm = [chainMap[df.iloc[row, 0]] for row in range(len(df.index))]

    df.insert(1, 'Tm', tm)

    df.to_csv(fileName.replace('Standings', 'StandingsAbbrev'))


def main():
    add_abbreviated_team_names(fileName)


if __name__ == '__main__':
    main()
