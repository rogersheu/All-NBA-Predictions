from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transfer_data import *


def XGBoost(X, y, X_2022):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # No scaling required

    xg = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)

    # xg = GradientBoostingClassifier(tree_method=hist, grow_policy=lossguide, eta=0.1, gamma=1.0, max_depth=0, max_leaves=255, min_child_weight=100)

    xg.fit(X_train, y_train)

    y_pred = xg.predict(X_test)

    print('Confusion matrix and classification report for XGBoost model.\n')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    
    y_2022 = xg.predict(X_2022)
    predictions = xg.predict_proba(X_2022)

    return predictions[:,1]

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    XGBoost(X, y, X_2022)

if __name__ == "__main__":
    main()