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

def get_all_player_stats():
    print("Pick your file containing stats for all players to train/test the model.")
    df = pd.read_csv(pick_file())
    X = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]
    y = df['allLeague']

    return X, y


def get_2022_stats(fileName):
    print("Pick your file containing this season's stats for prediction.")
    df = pd.read_csv(fileName)
    X_predict = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]

    return X_predict

def addtodf_savetoCSV(fileName: str, classifierName: str, classifierData: pd.Series, classifierProbName: str, classifierProbData: pd.Series, modelType: str):
    df = pd.read_csv(fileName)
    df[classifierName] = classifierData.round(2)
    df[classifierProbName] = classifierProbData.round(2)
    df.sort_values(by = classifierProbName, ascending = False, inplace = True)
    fileName = fileName.replace(".csv","")
    fileName = f"{fileName}_{modelType}.csv"
    df.to_csv(fileName)


def probabilityonly_toCSV(fileName: str, probName: str, probData: pd.Series):
    df = pd.read_csv(fileName)
    df[probName] = probData.round(2)
    # df.sort_values(by = probName, ascending = False, inplace = True)
    df.to_csv(fileName)


def sortCSV(fileName):
    df = pd.read_csv(fileName) 
    df.sort_values(by = df[['RF','SVM','kNN']].mean(axis=0), ascending = False, inplace = True) # df.iloc[:,['RF','SVM','kNN']].mean(axis=0) probably works too
    df.to_csv(fileName)
    