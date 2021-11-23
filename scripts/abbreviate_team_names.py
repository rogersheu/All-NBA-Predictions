import team_mapping
import pandas as pd
import collections


def add_abbreviated_team_names():
    df = pd.read_csv('baseData/teamStandings.csv', delimiter=',')

    chainMap = collections.ChainMap(team_mapping.activeTeams, team_mapping.tradedPlayers, team_mapping.defunctTeams)

    tm = [chainMap[df.iloc[row,0]] for row in range(len(df.index))]
        

    # print(tm)

    df.insert(1, 'Tm', tm)

    df.to_csv('baseData/teamStandingsAbbrev.csv')

add_abbreviated_team_names()