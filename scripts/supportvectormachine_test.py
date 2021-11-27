from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def SVM(predictorArray, classlabelArray):

    X = predictorArray
    y = classlabelArray

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    cols = X_train.columns
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)
    X_train = pd.DataFrame(X_train, columns=[cols])
    X_test = pd.DataFrame(X_test, columns=[cols])

    # # instantiate classifier with default hyperparameters
    # svc=SVC() 


    # # fit classifier to training set
    # svc.fit(X_train,y_train)


    # # make predictions on test set
    # y_pred=svc.predict(X_test)
    
    # # compute and print accuracy score
    # print('Model accuracy score with default hyperparameters: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))


    # # instantiate classifier with rbf kernel and C=100
    # svc=SVC(C=100.0) 


    # # fit classifier to training set
    # svc.fit(X_train,y_train)


    # # make predictions on test set
    # y_pred=svc.predict(X_test)


    # # compute and print accuracy score
    # print('Model accuracy score with rbf kernel and C=100.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))


    # # instantiate classifier with rbf kernel and C=1000
    # svc=SVC(C=1000.0) 


    # # fit classifier to training set
    # svc.fit(X_train,y_train)


    # # make predictions on test set
    # y_pred=svc.predict(X_test)


    # # compute and print accuracy score
    # print('Model accuracy score with rbf kernel and C=1000.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))


    # instantiate classifier with linear kernel and C=1.0
    linear_svc=SVC(kernel='linear', C=1.0) 


    # fit classifier to training set
    linear_svc.fit(X_train,y_train)


    # make predictions on test set
    y_pred_test=linear_svc.predict(X_test)


    # compute and print accuracy score
    print('Model accuracy score with linear kernel and C=1.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred_test)))    



    # instantiate classifier with linear kernel and C=100.0
    linear_svc100=SVC(kernel='linear', C=100.0) 


    # fit classifier to training set
    linear_svc100.fit(X_train, y_train)


    # make predictions on test set
    y_pred=linear_svc100.predict(X_test)


    # compute and print accuracy score
    print('Model accuracy score with linear kernel and C=100.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))

    # instantiate classifier with linear kernel and C=1000.0
    linear_svc1000=SVC(kernel='linear', C=1000.0) 


    # fit classifier to training set
    linear_svc1000.fit(X_train, y_train)


    # make predictions on test set
    y_pred=linear_svc1000.predict(X_test)


    # compute and print accuracy score
    print('Model accuracy score with linear kernel and C=1000.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))

    y_pred_train = linear_svc.predict(X_train)

    print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train)))

    # print the scores on training and test set

    print('Training set score: {:.4f}'.format(linear_svc.score(X_train, y_train)))

    print('Test set score: {:.4f}'.format(linear_svc.score(X_test, y_test)))


    null_accuracy = y_test.value_counts()[0] / (y_test.value_counts()[0] + y_test.value_counts()[1])
    print('Null accuracy score: {0:0.4f}'. format(null_accuracy))


def main():
    df = pd.read_csv("/baseData/allplayers_statsfromSQL.csv")
    df.isnull().sum()
    X = df[['RPG','APG','SBPG','PPG','TS','WS48','Perc']]
    y = df['allLeague']
    SVM(X, y)

if __name__ == "__main__":
    main()