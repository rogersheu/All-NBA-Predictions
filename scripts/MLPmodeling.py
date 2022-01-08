# Potential improvements: Refining of hyperparameters, hidden layer sizes, alpha, learning rate, etc.
# Tried implementing MLP in Keras/Tensorflow BUT Python 3.10 not supported for Tensorflow yet (only up to 3.8)
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from transfer_data import *
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

# MLP = Multi-layer perceptron
def MLP(X, y, X_2022):
    iterations = 10 # Number of trials
    prediction_trials = []
    scaler = StandardScaler()
    clf = MLPClassifier(max_iter = 1000, hidden_layer_sizes = (2,2), solver = "adam")

    # Max_iter was changed from its default of 200 to 1000. May need to be changed in the future.
    # Activation of 'tanh' was just a tad better than 'relu'
    for i in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)

        # MLP are sensitive to feature scaling

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        X_2022_forfit = scaler.transform(X_2022)

        clf.fit(X_train, y_train)

        # Generating confusion matrix and classification report
        y_true, y_pred = y_test, clf.predict(X_test)

        prediction_trials.append(clf.predict_proba(X_2022_forfit)[:,1])

    print('Confusion matrix and classification report for Multilayer Perceptron model, final iteration.\n')
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred))

    df = pd.DataFrame(prediction_trials).transpose()

    return df.mean(axis=1)


    #####
    ### If running this function alone
    # addtodf_savetoCSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], 'MLP')


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    MLP(X, y, X_2022)

if __name__ == "__main__":
    main()