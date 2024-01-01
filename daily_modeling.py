import sys
import warnings

import pandas as pd

from models.GBMmodeling import GBM
from models.kNNmodeling import kNN
from models.MLPmodeling import MLP
from models.RFmodeling import RF
from models.SVMmodeling import SVM
from models.XGBoostmodeling import XGBoost
from utils.transfer_data import (
    get_2022_stats,
    get_all_player_stats,
    pick_file,
    postprocessing,
)


def warn(*args, **kwargs):
    pass


warnings.warn = warn


def file_load(filePath):
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats(filePath)
    return X, y, X_2022


def full_modeling(srcFile, X, y, X_2022):
    df = pd.read_csv(srcFile)
    df["RF"] = RF(X, y, X_2022)
    df["SVM"] = SVM(X, y, X_2022)
    df["kNN"] = kNN(X, y, X_2022)
    df["MLP"] = MLP(X, y, X_2022)
    df["GBM"] = GBM(X, y, X_2022)
    df["XGB"] = XGBoost(X, y, X_2022)
    return df


def model_one_file():
    print("Pick your file containing this season's stats for prediction.")
    file_path = pick_file()
    X, y, X_2022 = file_load(file_path)
    df = full_modeling(file_path, X, y, X_2022)

    dest_filename = file_path.replace(".csv", "")
    dest_filename = f"{dest_filename}_modeled.csv"
    df.to_csv(dest_filename)
    postprocessing(dest_filename)


def automated_modeling(start_date, end_date):
    # pd.date_range is inclusive
    for date in pd.date_range(start=start_date, end=end_date):
        date_str = date.strftime("%Y-%m-%d")
        date_nodash = date_str.replace("-", "")
        file_path = f"./data/dailystats/{date_str}/stats_{date_nodash}.csv"
        try:
            X, y, X_2022 = file_load(file_path)
        except FileNotFoundError:
            continue

        print(f"Starting model voting system for {date_str}.")
        df = full_modeling(file_path, X, y, X_2022)

        dest_filename = file_path.replace(".csv", "")
        dest_filename = f"{dest_filename}_modeled.csv"
        df.to_csv(dest_filename)
        postprocessing(dest_filename)
        print(f"Ensemble learning for {date_str} complete.")


# Expects either no argument (asks user to pick a file) OR -range YYYY-MM-DD YYYY-MM-DD (no quotes needed)
# Potential improvement: -quiet to hide classification matrices
def model_handler():
    args = sys.argv[1:]
    if len(args) == 0:
        model_one_file()
    elif args[0] == "-range":
        automated_modeling(args[1], args[2])
    else:
        print("Please enter the correct arguments.")


if __name__ == "__main__":
    model_handler()
