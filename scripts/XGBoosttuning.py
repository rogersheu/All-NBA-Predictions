import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from transfer_data import *


# Most important hyperparameters, according to https://towardsdatascience.com/mastering-xgboost-2eb6bce6bc76

# (1) how many sub-trees to train; 
# (2) the maximum tree depth (a regularization hyperparameter); 
# (3) the learning rate; 
# (4) the L1 (reg_alpha) and L2 (reg_ lambda) regularization rates that determine the extremity of weights on the leaves; 
# (5) the complexity control (gamma=γ), a pseudo- regularization hyperparameter; 
# (6) minimum child weight

iterations = 10

def XGBoost(X, y, X_2022):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)
    xgb_model = xgb.XGBClassifier()

# https://xgboost.readthedocs.io/en/latest/parameter.html#learning-task-parameters
    parameter_space = {
        "objective" : [],
        "eval_metric" : [],
# 'gpu-hist' fastest, requires CUDA
# 'exact' most accurate but slowest
# 'approx' for larger datasets
# 'auto' is default (picks one)
# 'hist' is much faster, good for large datasets
        "tree_method" : ['hist'], 
        "n_estimators" : [100], #1
        "max_depth" : [], #2
# 3. eta, aka learning rate, default is 0.3
# too high and you risk overfitting and bypassing minima
# too low and it takes longer to learn, aka more iterations
        "eta" : [0.01, 0.015, 0.025, 0.05, 0.1, 0.2, 0.3, 0.5, 1],
        "alpha" : [],
        "lambda" : [],
        "gamma" :  [], #5, min_split_loss
# 6. Minimum child weight, a child needs the threshold weight (Hessian) to continue being considered
        "min_child_weight" : [1, 3, 5, 7]
    }

    scores = ["precision", "recall"]

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(xgb_model, parameter_space, scoring="%s_macro" % score, n_jobs = -1, cv = 3) 
        # clf = RandomizedSearchCV(MLPmodel, parameter_space, scoring="%s_macro" % score, n_jobs = -1, cv = 3) 
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

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    XGBoost(X, y, X_2022)

if __name__ == "__main__":
    main()