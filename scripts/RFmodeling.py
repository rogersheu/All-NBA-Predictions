import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from transfer_data import get_ML_data 

def RF(predictorArray, classlabelArray):

    X = predictorArray
    y = classlabelArray

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    clf = RandomForestClassifier(n_estimators = 1000, random_state = 0)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


    feature_imp = pd.Series(clf.feature_importances_,index=X.columns.values).sort_values(ascending=False)
    print(feature_imp)

    df2022 = pd.read_csv("./baseData/ML/players2022_forprediction.csv")
    
    X_2022 = df2022[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]

    y_2022 = clf.predict(X_2022)


    classifier = clf.fit(X_2022,y_2022)
    predictions = classifier.predict_proba(X_2022)
    
    df2022['allLeague'] = y_2022

    df2022['probabilityFor'] = predictions[:,1]
    # df2022['probAgainst'] = predictions[:,0]

    df2022.sort_values(by = ['probabilityFor'], ascending = False, inplace = True)

    df2022.to_csv("./baseData/ML/players2022_predicted.csv")

def main():
    X, y = get_ML_data()
    RF(X, y)

if __name__ == "__main__":
    main()