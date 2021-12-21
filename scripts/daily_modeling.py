def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from SVMmodeling import SVM
from kNNmodeling import kNN
from RFmodeling import RF
from MLPmodeling import MLP
from XGBoostmodeling import XGBoost
from transfer_data import *


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    print("Please pick the data file you want to append this to.")
    srcFile = pick_file()
    newFileName = srcFile.replace(".csv","")
    newFileName = f"{newFileName}_modeled.csv"
    df = pd.read_csv(srcFile)
    df['RF'] = RF(X, y, X_2022)
    df['SVM'] = SVM(X, y, X_2022)
    df['kNN'] = kNN(X, y, X_2022)
    df['MLP'] = MLP(X, y, X_2022)
    df['XGBoost'] = XGBoost(X, y, X_2022)
    df.to_csv(newFileName)
    sortCSV(newFileName)

if __name__ == "__main__":
    main()