import pandas as pd


def get_ML_data():
    df = pd.read_csv("./baseData/allPlayers_statsfromSQL.csv")
    X = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]
    y = df['allLeague']

    return X, y