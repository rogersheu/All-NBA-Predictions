from SVMmodeling import SVM
from kNNmodeling import kNN
from RFmodeling import RF
from MLPmodeling import MLP
from GBMmodeling import GBM
from XGBoostmodeling import XGBoost

from transfer_data import *
import sys
import warnings
from datetime import datetime

def warn(*args, **kwargs):
    pass
warnings.warn = warn

def file_load(filePath):
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats(filePath)
    return X, y, X_2022

def ensemble_modeling(srcFile, X, y, X_2022):
    df = pd.read_csv(srcFile)
    df['RF'] = RF(X, y, X_2022)
    df['SVM'] = SVM(X, y, X_2022)
    df['kNN'] = kNN(X, y, X_2022)
    df['MLP'] = MLP(X, y, X_2022)
    df['GBM'] = GBM(X, y, X_2022)
    df['XGB'] = XGBoost(X, y, X_2022)
    return df

def model_one_file():
    print("Pick your file containing this season's stats for prediction.")
    filePath = pick_file()
    X, y, X_2022 = file_load(filePath)
    df = ensemble_modeling(filePath, X, y, X_2022)

    newFileName = filePath.replace(".csv","")
    newFileName = f"{newFileName}_modeled.csv"
    df.to_csv(newFileName)
    postprocessing(newFileName)

def automated_modeling(startDate, endDate):
    for date in pd.date_range(start=startDate, end=endDate): # pd.date_range is inclusive
        date_str = date.strftime("%Y-%m-%d")
        date_nodash = date_str.replace("-", "")
        filePath = f"./baseData/dailystats/{date_str}/stats_{date_nodash}.csv"
        try:
            X, y, X_2022 = file_load(filePath)
        except FileNotFoundError:
            continue
        
        print(f"Starting ensemble learning for {date_str}.")
        df = ensemble_modeling(filePath, X, y, X_2022)
        
        newFileName = filePath.replace(".csv","")
        newFileName = f"{newFileName}_modeled.csv"
        df.to_csv(newFileName)
        postprocessing(newFileName)
        print(f"Ensemble learning for {date_str} complete.")

# Expects either no argument (asks user to pick a file) OR -range YYYY-MM-DD YYYY-MM-DD (no quotes needed)
def main():
    args = sys.argv[1:]
    # if args[0] == '-single':
    if len(args) == 0:
        model_one_file()
    elif args[0] == '-range':
        automated_modeling(args[1], args[2])
    else:
        print("Please enter the correct arguments.")
        return False

if __name__ == "__main__":
    main()