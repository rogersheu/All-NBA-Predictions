# Potential improvements: Refining of hyperparameters, hidden layer sizes, alpha, learning rate, etc.

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from transfer_data import *
from sklearn.metrics import classification_report

# MLP = Multi-layer perceptron
def MLP(X, y, X_2022):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    # MLP are sensitive to feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)    

    # MLPmodel = MLPClassifier()
    # # As a personal reminder, activation refers to the output function behavior
    # #   logistic is logistic: 1/(1+e^-x)
    # #   tanh is just the trig function
    # #   relu is the piecewise x negative -> 0, x positive -> x
    # # Solver refers to the algorithm used
    # # Alpha is the L2 penalty hyperparameter factor. L2 is the penalty assigned
    # #   to the error term, given by the L2 norm (sqrt of the residual sums squared)
    # #
    # # Learning rate: adaptive adjusts the learning rate (presumably the impulse generated
    # # from the gradient descent) lower if it is shooting too far.
    # parameter_space = { 
    #     'hidden_layer_sizes': [(25,20,25), (10,50,10), (100,)],
    #     'activation': ['tanh', 'relu'], 
    #     'solver': ['lbfgs', 'sgd', 'adam'],
    #     'alpha': [0.0001, 0.05],
    #     'learning_rate': ['constant','adaptive']
    # }
    # clf = GridSearchCV(MLPmodel, parameter_space, n_jobs = -1, cv = 3) 

    clf = MLPClassifier(max_iter = 1000, hidden_layer_sizes = (10,50,10))
    clf.fit(X_train, y_train)


    # Best paramete set
    # print('Best parameters found:\n', clf.best_params_)

    # # All results
    # means = clf.cv_results_['mean_test_score']
    # stds = clf.cv_results_['std_test_score']
    # for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    #     print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

    y_true, y_pred = y_test, clf.predict(X_test)

    print('Results on the test set for the multilayer perceptron (MLP):')
    print(classification_report(y_true, y_pred))


    X_2022 = scaler.transform(X_2022)
    y_2022 = clf.predict(X_2022)

    predictions = clf.predict_proba(X_2022)

    return predictions[:,1]

    # addtodf_savetoCSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], 'MLP')


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    MLP(X, y, X_2022)

if __name__ == "__main__":
    main()