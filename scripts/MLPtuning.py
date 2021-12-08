from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from transfer_data import *
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    parameter_space = { 
        "hidden_layer_sizes" : [(2), (3), (4), (5), (6), (2,2), (3,3)],
        "solver" : ['lbfgs', 'sgd', 'adam'],
        "alpha" : [0.0001, 0.001, 0.01],
        "learning_rate" : ['constant', 'invscaling', 'adaptive']
    }
    
    MLPmodel = MLPClassifier(max_iter = 2000)

    scores = ["precision", "recall"]

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(MLPmodel, parameter_space, scoring="%s_macro" % score, n_jobs = -1, cv = 3) 
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_["mean_test_score"]
        if score == "precision":
            precision_means = means
        else:
            recall_means = means
        stds = clf.cv_results_["std_test_score"]
        for mean, std, params in zip(means, stds, clf.cv_results_["params"]):
            print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()


    plt.plot(precision_means, recall_means)
    plt.show()

def main():
    X, y = get_all_player_stats()
    MLP_tuning(X, y)

if __name__ == "__main__":
    main()



