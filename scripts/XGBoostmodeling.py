from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transfer_data import *


def XGBoost(X, y, X_2022):
    iterations = 10
    prediction_trials = []
    # No scaling required
    for i in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)
        xg = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)

        # Possible hyperparameters
        # xg = GradientBoostingClassifier(tree_method=hist, grow_policy=lossguide, eta=0.1, gamma=1.0, max_depth=0, max_leaves=255, min_child_weight=100)

        xg.fit(X_train, y_train)

        y_pred = xg.predict(X_test)


        prediction_trials.append(xg.predict_proba(X_2022)[:,1])


    print(f'Confusion matrix and classification report for XGBoost model, final iteration.\n')
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