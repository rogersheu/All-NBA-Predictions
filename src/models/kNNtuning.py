from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from src.utils.transfer_data import get_2022_stats
from src.utils.transfer_data import get_all_player_stats


def kNN(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # [n_neighbors, p] = 81, 1 best for precision
    # [n_neighbors, p] = 5, 2 best for recall
    parameter_space = {
        'n_neighbors': list(range(1, 101, 1)),
        'p': [1, 2],  # p=1 is Manhattan distance, p=2 is Euclidean, p=2 is default
    }

    kNNmodel = KNeighborsClassifier()

    scores = ['precision', 'recall']

    for score in scores:
        print('# Tuning hyper-parameters for %s' % score)
        print()

        clf = GridSearchCV(
            kNNmodel, parameter_space,
            scoring='%s_macro' % score, n_jobs=-1, cv=3,
        )
        clf.fit(X_train, y_train)

        print('Best parameters set found on development set:')
        print()
        print(clf.best_params_)
        print()
        print('Grid scores on development set:')
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print('{:0.3f} (+/-{:0.03f}) for {!r}'.format(mean, std * 2, params))
        print()

        print('Detailed classification report:')
        print()
        print('The model is trained on the full development set.')
        print('The scores are computed on the full evaluation set.')
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()


def main():
    X, y = get_all_player_stats()
    kNN(X, y)


if __name__ == '__main__':
    main()
