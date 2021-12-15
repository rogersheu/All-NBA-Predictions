from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from transfer_data import *
# from sklearn.calibration import calibration_curve
# import matplotlib.pyplot as plt


# Next thing to implement is GridSearchCV
# https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

def RF(X, y, X_2022): # Change to take in a csv and output a csv
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Tried changing hyperparameters, see RFtuning.py, with default settings having the best accuracy
    randomforest = RandomForestClassifier(n_estimators = 100, random_state = 0)

    randomforest.fit(X_train, y_train)

    y_pred = randomforest.predict(X_test)

    print('Confusion matrix and classification report for Random Forest model.\n')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    
    # y_means, proba_means = calibration_curve(y_pred, randomforest.predict_proba(X_test)[:,1], n_bins = 7, strategy = 'uniform')
    # plt.plot([0, 1], [0, 1], linestyle = '--', label = 'Perfect calibration')
    # plt.plot(proba_means, y_means)

    # feature_imp = pd.Series(randomforest.feature_importances_,index=X.columns.values).sort_values(ascending=False)
    # print(feature_imp)

    # Making predictions
    y_2022 = randomforest.predict(X_2022)

    predictions = randomforest.predict_proba(X_2022)

    return predictions[:,1]

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    RF(X, y, X_2022)

if __name__ == "__main__":
    main()