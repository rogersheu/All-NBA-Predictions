from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from utils.transfer_data import get_2022_stats
from utils.transfer_data import get_all_player_stats

# from sklearn.metrics import accuracy_score
# import seaborn as sn
# import matplotlib.pyplot as plt


def SVM(X, y, X_2022):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=0,
        stratify=y,
    )

    # Scaling to bring all columns to mean of 0 and unit variance
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Tried rbf (Gaussian), but linear was still more accurate.
    # Tried a variety of C from 10^-5 to 1000 and 0.1 was the most accurate
    linSVCmodel = SVC(kernel="linear", C=0.1, probability=True, random_state=0)
    linSVCmodel.fit(X_train, y_train)
    y_pred = linSVCmodel.predict(X_test)

    print("Confusion matrix and classification report for SVM model.\n")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # df_cm = pd.DataFrame(confusion_matrix(y_test, y_pred), range(2), range(2))
    # sn.set(font_scale=1.4)
    # sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    # plt.show()

    # Difference in model accuracy between C = 100 and C = 1000 was minimal. Slight improvement from 1 to 100.

    # Must scale prior to use
    X_2022 = scaler.transform(X_2022)
    y_2022 = linSVCmodel.predict(X_2022)

    predictions = linSVCmodel.predict_proba(X_2022)

    return predictions[:, 1]


if __name__ == "__main__":
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    SVM(X, y, X_2022)
