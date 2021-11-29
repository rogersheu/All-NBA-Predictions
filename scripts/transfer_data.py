from typing import Tuple
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# dataSrc_all = "./baseData/ML/allPlayers_paceadjusted_statsfromSQL.csv"

def pick_file():
    root = tk.Tk()
    root.withdraw()

    filePathName = filedialog.askopenfilename()

    return filePathName

def get_allplayerstats():
    print("Pick your file containing stats for all players to train/test the model.")
    df = pd.read_csv(pick_file())
    X = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]
    y = df['allLeague']

    return X, y


def get_2022stats():
    print("Pick your file containing this season's stats for prediction.")
    df = pd.read_csv(pick_file())
    X_predict = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]

    return X_predict

def addandsave_to_CSV(fileName: str, rfcName: str, rfcData: pd.Series, rfcProbName: str, rfcProbData: pd.Series):
    df = pd.read_csv(fileName)
    df[rfcName] = rfcData
    df[rfcProbName] = rfcProbData
    df.sort_values(by = rfcProbName, ascending = False, inplace = True)
    print(df)
    df.to_csv(fileName.replace("forpredicting", "predicted")) # Relies on original file having "_forpredicting" in the file name.