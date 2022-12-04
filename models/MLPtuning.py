import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from utils.transfer_data import get_all_player_stats


# As a personal reminder, activation refers to the output function behavior
#   logistic is logistic: 1/(1+e^-x)
#   tanh is just the trig function
#   relu is the piecewise x negative -> 0, x positive -> x
# Solver refers to the algorithm used
# Alpha is the L2 penalty hyperparameter factor. L2 is the penalty assigned
#   to the error term, given by the L2 norm (sqrt of the residual sums squared)
#
# Learning rate: adaptive adjusts the learning rate (presumably the impulse generated
# from the gradient descent) lower if it is shooting too far.
#
# parameter_space = {
#     'hidden_layer_sizes': [(25,20,25), (10,50,10), (100,)], # does not need to be this large for this particular data set
#     'activation': ('tanh', 'relu'), # Relu seems to be the preferred method nowadays
#     'solver': ('lbfgs', 'sgd', 'adam'),
#     'alpha': [0.0001, 0.05],
#     'learning_rate': ('constant','adaptive')
# }


def MLP_tuning(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Picked 'relu' instead of 'tanh', very similar results either way
    # Tried various alpha, reverting to the default of 0.0001
    # 'sgd' (stochastic gradient descent) had the worst performance out of the three, and learning_rate is dependent on its usage

    # Picked hidden layer of 2 nodes and solver as 'adam' after multiple iterations
    # Expecting precision near 0.89 and recall near 0.86
    parameter_space = {
        'hidden_layer_sizes': [(2), (3), (4), (5), (2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)],
        'solver': ['lbfgs', 'adam'],
    }

    MLPmodel = MLPClassifier(max_iter=2000)

    scores = ['precision', 'recall']

    for score in scores:
        print('# Tuning hyper-parameters for %s' % score)
        print()

        clf = GridSearchCV(
            MLPmodel, parameter_space,
            scoring='%s_macro' % score, n_jobs=-1, cv=3,
        )
        # clf = RandomizedSearchCV(MLPmodel, parameter_space, scoring="%s_macro" % score, n_jobs = -1, cv = 3)
        clf.fit(X_train, y_train)

        print('Best parameters set found on development set:')
        print()
        print(clf.best_params_)
        print()
        print('Grid scores on development set:')
        print()
        means = clf.cv_results_['mean_test_score']
        if score == 'precision':
            precision_means = means
        else:
            recall_means = means
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

    plt.scatter(precision_means, recall_means)
    plt.show()


if __name__ == '__main__':
    X, y = get_all_player_stats()
    MLP_tuning(X, y)
