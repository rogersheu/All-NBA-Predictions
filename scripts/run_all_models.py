from tkinter.constants import Y
from SVMmodeling import SVM
from kNNmodeling import kNN
from RFmodeling import RF
from MLPmodeling import MLP
from transfer_data import *


def main():
    X, y = get_all_player_stats()
    print("Where would you like to save the data?")
    destFile = pick_file()
    destFile = destFile.replace(".csv","")
    destFile = f"{destFile}_modeled.csv"    
    probabilityonly_toCSV(destFile, "RF", RF(X, y))
    probabilityonly_toCSV(destFile, "SVM", SVM(X, y))
    probabilityonly_toCSV(destFile, "kNN", kNN(X, y))
    probabilityonly_toCSV(destFile, "MLP", MLP(X, y))

    sortCSV(destFile)

if __name__ == "__main__":
    main()