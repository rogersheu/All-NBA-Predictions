import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

iterations = 10


def GBM(X, y, X_2022):
    prediction_trials = []
    # No scaling required
    for _ in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            stratify=y,
        )
        gbm_model = GradientBoostingClassifier(n_estimators=100)
        gbm_model.fit(X_train, y_train)
        y_pred = gbm_model.predict(X_test)

        prediction_trials.append(gbm_model.predict_proba(X_2022)[:, 1])

    print(
        "Confusion matrix and classification report for Gradient Boosted Trees model, final iteration.\n"
    )
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    df = pd.DataFrame(prediction_trials).transpose()

    return df.mean(axis=1)  # Average of the <iteration> trials.
