from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from transfer_data import get_ML_data 

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

    ##### Blueprint for this code is from https://www.kaggle.com/prashant111/svm-classifier-tutorial

    # Instantiate classifier with linear kernel and C=1.0
    linear_svc=svm.SVC(kernel='linear', C=1.0) 
    linear_svc.fit(X_train,y_train)
    y_pred_test=linear_svc.predict(X_test)

    # Compute and print accuracy score
    print('Model accuracy score with linear kernel and C=1.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred_test)))    

    # Instantiate classifier with linear kernel and C=100.0
    linear_svc100=svm.SVC(kernel='linear', C=100.0) 
    linear_svc100.fit(X_train, y_train)
    y_pred=linear_svc100.predict(X_test)

    # Compute and print accuracy score
    print('Model accuracy score with linear kernel and C=100.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))

    # Instantiate classifier with linear kernel and C=1000.0
    linear_svc1000=svm.SVC(kernel='linear', C=1000.0) 
    linear_svc1000.fit(X_train, y_train)
    y_pred=linear_svc1000.predict(X_test)
    print('Model accuracy score with linear kernel and C=1000.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred)))


    y_pred_train = linear_svc.predict(X_train)
    print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train)))

    # Print the scores on training and test set
    print('Training set score: {:.4f}'.format(linear_svc.score(X_train, y_train)))
    print('Test set score: {:.4f}'.format(linear_svc.score(X_test, y_test)))

    null_accuracy = y_test.value_counts()[0] / (y_test.value_counts()[0] + y_test.value_counts()[1])
    print('Null accuracy score: {0:0.4f}'. format(null_accuracy))


def main():
    X, y = get_ML_data()
    SVM(X, y)

if __name__ == "__main__":
    main()