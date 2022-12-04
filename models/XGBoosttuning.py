import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from utils.transfer_data import get_all_player_stats


# Most important hyperparameters, according to https://towardsdatascience.com/mastering-xgboost-2eb6bce6bc76

# (1) how many sub-trees to train;
# (2) the maximum tree depth (a regularization hyperparameter);
# (3) the learning rate;
# (4) the L1 (reg_alpha) and L2 (reg_ lambda) regularization rates that determine the extremity of weights on the leaves;
# (5) the complexity control (gamma=γ), a pseudo- regularization hyperparameter;
# (6) minimum child weight


# objective
# multi:softmax and multi:softprob seem to be popular, but this is not a multiclass problem


# tree_method
# 'gpu-hist' fastest, requires CUDA
# 'exact' most accurate but slowest
# 'approx' for larger datasets
# 'auto' is default (picks one)
# 'hist' is much faster, good for large datasets


# 3. eta, aka learning rate, default is 0.3
# too high and you risk overfitting and bypassing minima
# too low and it takes longer to learn, aka more iterations

# 4. Increasing alpha or lambda will make the model more conservative.

# 5, min_split_loss
# 6. Minimum child weight, a child needs the threshold weight (Hessian) to continue being considered


iterations = 10


def XGBoost(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y,
    )
    xgb_model = xgb.XGBClassifier(
        objective='binary:logistic',
        tree_method='hist',
        eval_metric='logloss',
        use_label_encoder=False,
        n_estimators=100,
        # eta = 0.2,
        # reg_alpha = 0
    )
    # https://xgboost.readthedocs.io/en/latest/parameter.html#learning-task-parameters
    parameter_space = {
        # "objective" : ['reg:squarederror', 'reg:squaredlogerror', 'reg:logistic', 'binary:logistic', 'binary:logitraw'],
        # "eval_metric" : ['rmse', 'logloss', 'error', 'aucpr'],
        # "n_estimators" : [25, 50, 100], #1
        # "max_depth" : [3, 4, 5, 6], #2
        'learning_rate': [0.1, 0.15, 0.2, 0.25, 0.3],  # 3
        # "reg_alpha" : [0, 0.1], #4
        'reg_lambda': [0.1, 0.5, 1, 2, 5, 10],  # 4
        'gamma': [0, 0.1, 0.2, 0.5, 1],  # 5
        # "min_child_weight" : [1, 3, 5, 7, 9] #6
    }

    # Through tuning these parameters in GridSearch

    # max_depth got worse as it increased. 3 was better than the default of 6.
    # eta = 0.25 (default is 0.3)
    # alpha = 0.1 (default is 0)
    # gamma = 0 (default)
    # lambda = 1 (default)

    # gamma has almost no effect on recall
    # n_estimators, more leads to higher recall in test set

    print('# Tuning hyper-parameters.\n')

    clf = GridSearchCV(xgb_model, parameter_space, scoring='f1_macro', cv=5)
    # clf = RandomizedSearchCV(xgb_model, parameter_space, n_iter = 100, scoring="%s_macro" % score, n_jobs = -1, cv = 3)
    clf.fit(X_train, y_train)

    print('Best parameters set found on development set:\n')
    print(clf.best_params_)
    print()
    print('Grid scores on development set:\n')

    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    params = clf.cv_results_['params']

    for mean, std, params in zip(means, stds, params):
        print('{:0.3f} (+/-{:0.03f}) for {!r}'.format(mean, std * 2, params))
    print()

    print('Detailed classification report:\n')
    print('The model is trained on the full development set.')
    print('The scores are computed on the full evaluation set.\n')
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))


if __name__ == '__main__':
    X, y = get_all_player_stats()
    XGBoost(X, y)
