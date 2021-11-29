import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from transfer_data import *

fileName = "./baseData/ML/stats_20211128.csv"

def RF(X, y): # Change to take in a csv and output a csv
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    randomforest = RandomForestClassifier(n_estimators = 100, random_state = 0)

    randomforest.fit(X_train, y_train)

    y_pred = randomforest.predict(X_test)

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    feature_imp = pd.Series(randomforest.feature_importances_,index=X.columns.values).sort_values(ascending=False)
    print(feature_imp)

    # Making predictions
    fileName = pick_file()  

    X_2022 = get_2022stats(fileName)
    y_2022 = randomforest.predict(X_2022)

    # classifier = randomforest.fit(X_2022,y_2022)
    predictions = randomforest.predict_proba(X_2022)
    addandsave_to_CSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], "RF")

def main():
    X, y = get_allplayerstats()
    RF(X, y)

if __name__ == "__main__":
    main()