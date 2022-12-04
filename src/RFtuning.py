from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from transfer_data import *


def RF_hyperparameter_tuning(X, y):  # Change to take in a csv and output a csv
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    parameter_space = {
        'max_depth': [2, 5, 10, 20, None],  # default is None
        'max_leaf_nodes': [5, 10, None],  # default is None
    }

    randomforest = RandomForestClassifier(n_estimators=100, random_state=0)

    scores = ['precision', 'recall']

    for score in scores:
        print('# Tuning hyper-parameters for %s' % score)
        print()

        clf = GridSearchCV(
            randomforest, parameter_space,
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
    RF_hyperparameter_tuning(X, y)


if __name__ == '__main__':
    main()
