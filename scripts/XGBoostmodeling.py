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
    xgb_model = xgb.XGBClassifier(tree_method = "hist") # Histogram-based boosting makes XGBoost much faster
    # Other speed-up options include using your CPU with CUDA (Nvidia)  xgb.XGBClassifier(tree_method = "gpu_hist")
    # and using single precision xgb.XGBClassifier(tree_method = "gpu_hist", single_precision_histogram=True)

    xgb_model.fit(X_train, y_train)
    y_pred = xgb_model.predict(X_test)

    print('Confusion matrix and classification report for XGBoost model.\n')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))



    predictions = xgb_model.predict_proba(X_2022)

    return predictions[:,1]


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    XGBoost(X, y, X_2022)

if __name__ == "__main__":
    main()