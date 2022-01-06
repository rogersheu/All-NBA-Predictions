from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from transfer_data import *
import matplotlib.pyplot as plt

### Results from different hyperparameter combinations (perhaps randomized) to form an ensemble
# Wenzel et al. 2020, Hyperparameter Ensembles for Robustness and Uncertainty Quantification, https://arxiv.org/abs/2006.13570

def gradientboosted_tuning(X, y):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)
    
    parameter_space = { 
        "learning_rate" : [0.01, 0.05, 0.1, 0.25, 0.5],
        #"min_samples_split" : [],
        #"min_samples_leaf" : [],
        "max_depth" : [3, 5, 7, 9],
        #"max_leaf_nodes" : [],
        #"max_features" : [],
        "n_estimators": [50, 100, 200]
    }
    
    # Option to use HistGradientBoostingClassifier
    gbm_model = GradientBoostingClassifier()

    scores = ["precision", "recall"]

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(gbm_model, parameter_space, scoring = "f1") #"%s_macro" % score, cv = 5) 
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:\n")
        print(clf.best_params_)
        print("\nGrid scores on development set:\n")
        means = clf.cv_results_["mean_test_score"]
        stds = clf.cv_results_["std_test_score"]

        for mean, std, params in zip(means, stds, clf.cv_results_["params"]):
            print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        print()

        print("Detailed classification report:\n")
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.\n")
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))

def main():
    X, y = get_all_player_stats()
    gradientboosted_tuning(X, y)

if __name__ == "__main__":
    main()