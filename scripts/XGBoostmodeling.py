import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transfer_data import *

iterations = 10

def XGBoost(X, y, X_2022):

    iterations = 10 # Number of trials
    prediction_trials = []

    for i in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)
        xgb_model = xgb.XGBClassifier(
            objective = 'binary:logistic',
            tree_method = 'hist',
            eval_metric = 'logloss',  
            use_label_encoder = False, 
            n_estimators = 100, 
            learning_rate = 0.2, 
            gamma = 1,
            reg_lambda = 5,
            reg_alpha = 0,
        )
        # Histogram-based boosting makes XGBoost much faster
        # Other speed-up options include using your CPU with CUDA (Nvidia)  xgb.XGBClassifier(tree_method = "gpu_hist")
        # and using single precision xgb.XGBClassifier(tree_method = "gpu_hist", single_precision_histogram=True)

        xgb_model.fit(X_train, y_train)
        y_pred = xgb_model.predict(X_test)

        predictions = xgb_model.predict_proba(X_2022)
        prediction_trials.append(predictions[:,1])

    print('Confusion matrix and classification report for XGBoost model, final iteration.\n')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


    df = pd.DataFrame(prediction_trials).transpose()
    return df.mean(axis=1)

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    XGBoost(X, y, X_2022)

if __name__ == "__main__":
    main()