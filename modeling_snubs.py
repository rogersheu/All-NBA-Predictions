from models.kNNmodeling import kNN
from models.MLPmodeling import MLP
from models.RFmodeling import RF
from models.SVMmodeling import SVM
from utils.transfer_data import get_all_player_stats, pd, pick_file, sortCSV_historical


def main():
    X, y = get_all_player_stats()
    print("Please pick the data file you want to append this to.")
    srcFile = pick_file()
    newFileName = srcFile.replace(".csv", "")
    newFileName = f"{newFileName}_snubs.csv"
    df = pd.read_csv(srcFile)
    df["RF"] = RF(X, y, X)
    df["SVM"] = SVM(X, y, X)
    df["kNN"] = kNN(X, y, X)
    df["MLP"] = MLP(X, y, X)
    df.to_csv(newFileName)
    sortCSV_historical(newFileName)


if __name__ == "__main__":
    main()
