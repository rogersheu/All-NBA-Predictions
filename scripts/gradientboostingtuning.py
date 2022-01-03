from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from transfer_data import *

# Most important hyperparameters, according to https://towardsdatascience.com/mastering-xgboost-2eb6bce6bc76

# (1) how many sub-trees to train; 
# (2) the maximum tree depth (a regularization hyperparameter); 
# (3) the learning rate; 
# (4) the L1 (reg_alpha) and L2 (reg_ lambda) regularization rates that determine the extremity of weights on the leaves; 
# (5) the complexity control (gamma=γ), a pseudo- regularization hyperparameter; 
# (6) minimum child weight

### Results from different hyperparameter combinations (perhaps randomized) to form an ensemble
# Wenzel et al. 2020, Hyperparameter Ensembles for Robustness and Uncertainty Quantification, https://arxiv.org/abs/2006.13570

def gradientboosted_tuning(X, y, X_2022):
    iterations = 10
    prediction_trials = []
    # No scaling required
    for i in range(iterations):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify = y)
        gb = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1)

        # Possible hyperparameters
        gb = GradientBoostingClassifier(
            n_estimators = 100, #1
            max_depth = 0, #2
            learning_rate = 1.0, #3
            
            ccp_alpha = 0.0, #5

                
            min_child_weight=100)

        gb.fit(X_train, y_train)

        y_pred = gb.predict(X_test)


        prediction_trials.append(gb.predict_proba(X_2022)[:,1])
    



def main():
    X, y = get_all_player_stats()
    gradientboosted_tuning(X, y)

if __name__ == "__main__":
    main()