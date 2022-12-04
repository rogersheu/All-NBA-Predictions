import tkinter as tk
from tkinter import filedialog

import pandas as pd


# Dialog asks user to pick a file
def pick_file():
    try:
        root = tk.Tk()
        root.withdraw()

        filePathName = filedialog.askopenfilename()

        print('Thank you for picking a file!')
        return filePathName
    except FileNotFoundError:
        print('Please pick a valid file.')
        return False

# Dialog asks user to pick a path


def pick_path():
    try:
        root = tk.Tk()
        root.withdraw()
        pathName = filedialog.askdirectory()

        print('Thank you for picking a file path!')
        return pathName

    except ValueError:
        print('Please pick a valid path.')
        return False

# Loads stats from all seasons dating back to 1979-1980


def get_all_player_stats():
    # For manual selection of file.
    # print("Pick your file containing stats for all players to train/test the model.")
    # df = pd.read_csv(pick_file())
    #####

    fileName = './baseData/ML/all_stats_20211201.csv'
    df = pd.read_csv(fileName)
    print('All players data loaded.')

    X = df[['RPG', 'APG', 'SBPG', 'PPG', 'TS', 'WS48', 'Perc']]
    y = df['allLeague']

    return X, y

# Loads present season's stats


def get_2022_stats(filePath):
    df = pd.read_csv(filePath)
    X_predict = df[['RPG', 'APG', 'SBPG', 'PPG', 'TS', 'WS48', 'Perc']]

    return X_predict

# Only used when a single model is run and saved to a CSV


def addtodf_savetoCSV(fileName: str, classifierName: str, classifierData: pd.Series, classifierProbName: str, classifierProbData: pd.Series, modelType: str):
    df = pd.read_csv(fileName)
    df[classifierName] = classifierData.round(2)
    df[classifierProbName] = classifierProbData.round(2)
    df.sort_values(by=classifierProbName, ascending=False, inplace=True)
    fileName = fileName.replace('.csv', '')
    fileName = f'{fileName}_{modelType}.csv'
    df.to_csv(fileName)


def probabilityonly_toCSV(fileName: str, probName: str, probData: pd.Series):
    df = pd.read_csv(fileName)
    df[probName] = probData.round(2)
    # df.sort_values(by = probName, ascending = False, inplace = True)
    df.to_csv(fileName)

# Sorts by best model (by average proba)


def postprocessing(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[:, 1:]
    df = calculateAvg(df)
    df = sortbyAvg(df)
    df[['RF', 'SVM', 'MLP', 'GBM', 'XGB', 'Avg']] = df[[
        'RF', 'SVM', 'MLP', 'GBM', 'XGB', 'Avg',
    ]].round(3)
    df.to_csv(fileName, index=False)


def calculateAvg(df):
    df['Avg'] = (df['RF'] + df['SVM'] + df['GBM'] + df['XGB'] + df['MLP']) / 5
    return df


def sortbyAvg(df):
    df.sort_values(by='Avg', ascending=False, inplace=True)
    return df


def sortCSV_historical(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[:, 1:]
    df = average_and_deviation(df)
    df.sort_values(by='Avg', ascending=False, inplace=True)
    df[['SVM', 'kNN', 'MLP', 'Avg']] = df[[
        'SVM', 'kNN', 'MLP', 'Avg',
    ]].round(3)
    df.to_csv(fileName, index=False)


def average_and_deviation(df: pd.DataFrame):
    df['Avg'] = (df['RF'] + df['SVM'] + df['kNN'] + df['MLP']) / 4
    df['Deviation'] = (df['Avg'] - df['allLeague'])

    return df
