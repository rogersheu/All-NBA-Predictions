import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.metrics import accuracy_score
from transfer_data import *


def kNN(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    ## Framework from https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

    kNNmodel = KNeighborsClassifier(n_neighbors = 5)
    kNNmodel.fit(X_train, y_train)

    y_testpredicted = kNNmodel.predict(X_test)

    print(confusion_matrix(y_test, y_testpredicted))
    print(classification_report(y_test, y_testpredicted))

    fileName = pick_file()

    X_2022 = get_2022stats(fileName)

    # Must scale prior to use
    X_2022 = scaler.transform(X_2022)
    y_2022 = kNNmodel.predict(X_2022)

    predictions = kNNmodel.predict_proba(X_2022)

    addandsave_to_CSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], 'kNN')


def main():
    X, y = get_allplayerstats()
    kNN(X, y)

if __name__ == "__main__":
    main()