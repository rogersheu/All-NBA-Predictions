# Adds abbreviated team names (e.g., Los Angeles Lakers -> LAL) from team_mapping.py to the indicated csv
import collections

import pandas as pd
import team_mapping

filename = 'data/teamStandings.csv'


def add_abbreviated_team_names(filename):
    df = pd.read_csv(filename, delimiter=',')

    chainMap = collections.ChainMap(
        team_mapping.active_teams, team_mapping.traded_players, team_mapping.defunct_teams,
    )

    tm = [chainMap[df.iloc[row, 0]] for row in range(len(df.index))]

    df.insert(1, 'Tm', tm)

    df.to_csv(filename.replace('Standings', 'StandingsAbbrev'))


if __name__ == '__main__':
    add_abbreviated_team_names(filename)
