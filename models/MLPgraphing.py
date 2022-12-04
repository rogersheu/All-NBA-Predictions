import matplotlib.pyplot as plt
from sklearn.metrics import auc
from sklearn.metrics import precision_recall_curve
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


def MLP_graphing(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # parameter_space = {
    #     "hidden_layer_sizes" : [(4), (6), (8), (10), (3,3)],
    #     "activation" : ['tanh', 'relu'],
    #     "alpha" : [0.0001, 0.001],
    #     "learning_rate" : ['constant', 'invscaling', 'adaptive']
    # }

    # MLPmodel = MLPClassifier(max_iter = 2000)

    # clf = GridSearchCV(MLPmodel, parameter_space, n_jobs = -1, cv = 3)
    # clf.fit(X_train, y_train)

    clf = MLPClassifier(max_iter=1000, hidden_layer_sizes=(4))
    clf.fit(X_train, y_train)

    y_score = clf.predict_proba(X_test)[:, 1]

    precision, recall, thresholds = precision_recall_curve(y_test, y_score)
    plt.plot(recall, precision)
    plt.show()
    auc_precision_recall = auc(recall, precision)
    print(auc_precision_recall)
    # average_precision = average_precision_score(y_test, y_score)

    # disp = plot_precision_recall_curve(clf, X_test, y_test)
    # disp.ax_.set_title('Binary class Precision-Recall curve: '
    #                'AP={0:0.2f}'.format(average_precision))


#     plot-grid_search()


# def plot_grid_search(cv_results, grid_param_1, grid_param_2, name_param_1, name_param_2):
#     # Get Test Scores Mean and std for each grid search
#     scores_mean = cv_results['mean_test_score']
#     scores_mean = np.array(scores_mean).reshape(len(grid_param_2),len(grid_param_1))

#     scores_sd = cv_results['std_test_score']
#     scores_sd = np.array(scores_sd).reshape(len(grid_param_2),len(grid_param_1))

#     # Plot Grid search scores
#     _, ax = plt.subplots(1,1)

#     # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
#     for idx, val in enumerate(grid_param_2):
#         ax.plot(grid_param_1, scores_mean[idx,:], '-o', label= name_param_2 + ': ' + str(val))

#     ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
#     ax.set_xlabel(name_param_1, fontsize=16)
#     ax.set_ylabel('CV Average Score', fontsize=16)
#     ax.legend(loc="best", fontsize=15)
#     ax.grid('on')


if __name__ == '__main__':
    X, y = get_all_player_stats()
    MLP_graphing(X, y)
