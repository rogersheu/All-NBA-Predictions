# Potential improvements: Refining of hyperparameters, hidden layer sizes, alpha, learning rate, etc.
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from transfer_data import *
from sklearn.metrics import confusion_matrix, classification_report

# MLP = Multi-layer perceptron
def MLP(X, y, X_2022):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # MLP are sensitive to feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)    


    # Max_iter was changed from its default of 200 to 1000. May need to be changed in the future.
    # Activation of 'tanh' was just a tad better than 'relu'
    clf = MLPClassifier(max_iter = 1000, hidden_layer_sizes = (2), solver = "adam")
    clf.fit(X_train, y_train)

    y_true, y_pred = y_test, clf.predict(X_test)

    print('Confusion matrix and classification report for Multilayer Perceptron model.\n')
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred))


    X_2022 = scaler.transform(X_2022)
    y_2022 = clf.predict(X_2022)

    predictions = clf.predict_proba(X_2022)

    return predictions[:,1]

    # addtodf_savetoCSV(fileName, 'allLeague', y_2022, 'allLeague_prob', predictions[:,1], 'MLP')


def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    MLP(X, y, X_2022)

if __name__ == "__main__":
    main()