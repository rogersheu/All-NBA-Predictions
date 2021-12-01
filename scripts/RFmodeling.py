import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from transfer_data import *

# fileName = "./baseData/ML/stats_20211128.csv"

def RF(X, y, X_2022): # Change to take in a csv and output a csv
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    randomforest = RandomForestClassifier(n_estimators = 100, random_state = 0)

    randomforest.fit(X_train, y_train)

    y_pred = randomforest.predict(X_test)

    print("Model accuracy with Random Forest model:\n",metrics.accuracy_score(y_test, y_pred))

    feature_imp = pd.Series(randomforest.feature_importances_,index=X.columns.values).sort_values(ascending=False)
    print(feature_imp)

    # Making predictions
    y_2022 = randomforest.predict(X_2022)

    predictions = randomforest.predict_proba(X_2022)

    return predictions[:,1]

    # addtodf_savetoCSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], "RF")

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    RF(X, y, X_2022)

if __name__ == "__main__":
    main()