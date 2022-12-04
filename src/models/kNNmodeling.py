from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from src.utils.transfer_data import get_2022_stats
from src.utils.transfer_data import get_all_player_stats


def kNN(X, y, X_2022):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # More neighbors gives predict_proba a bit more nuance, though values will be slightly depressed
    # because of sparsity of true positives in the training data
    kNNmodel = KNeighborsClassifier(n_neighbors=75)
    kNNmodel.fit(X_train, y_train)

    y_pred = kNNmodel.predict(X_test)

    print('Confusion matrix and classification report for k-Nearest Neighbor model.\n')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Must scale prior to use
    X_2022 = scaler.transform(X_2022)
    y_2022 = kNNmodel.predict(X_2022)

    predictions = kNNmodel.predict_proba(X_2022)

    return predictions[:, 1]


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    kNN(X, y, X_2022)


if __name__ == '__main__':
    main()
