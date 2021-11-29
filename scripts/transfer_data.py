import pandas as pd
import tkinter as tk
from tkinter import filedialog

# dataSrc_all = "./baseData/ML/allPlayers_paceadjusted_statsfromSQL.csv"

def pick_file():
    try:
        root = tk.Tk()
        root.withdraw()

        filePathName = filedialog.askopenfilename()

        print("Thank you for picking a file!")
        return filePathName
    except FileNotFoundError:
        print("Please pick a valid file.")
        return False

def get_allplayerstats():
    print("Pick your file containing stats for all players to train/test the model.")
    df = pd.read_csv(pick_file())
    X = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]
    y = df['allLeague']

    return X, y


def get_2022stats(fileName):
    print("Pick your file containing this season's stats for prediction.")
    df = pd.read_csv(fileName)
    X_predict = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]

    return X_predict

def addandsave_to_CSV(fileName: str, rfcName: str, rfcData: pd.Series, rfcProbName: str, rfcProbData: pd.Series, modelType: str):
    df = pd.read_csv(fileName)
    df[rfcName] = rfcData.round(2)
    df[rfcProbName] = rfcProbData.round(2)
    df.sort_values(by = rfcProbName, ascending = False, inplace = True)
    fileName = fileName.replace(".csv","")
    fileName = f"{fileName}_{modelType}.csv"
    df.to_csv(fileName)