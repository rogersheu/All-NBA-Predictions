# Predicting All-Star/All-NBA Selections

Objective
===========
Using machine learning and deep learning models, identify players most likely to be selected onto either the NBA all-star team (halfway through the season) or an all-NBA team (at the end of the season). Inspiration and/or methodology from [here](https://www.reddit.com/r/nba/comments/bcdpls/oc_using_machine_learning_to_predict_the_2019_mvp/). Only the overarching information in that post was used. The code was written from scratch or sourced from unrelated analyses found online, especially scikit-learn's documentation.


Installation/Instructions
===========
Prerequisites: ```Python 3.10```, ```sqlite3```, ```DBeaver```
1. In order to use this program, either ```Clone``` the repository or ```download the ZIP file```. 
2. Go into python, change directory to this repository's folder in the GitHub folder (not any of the subfolders).
3. Get the full data by running ```python .\scripts\scrape_stats_cli.py -tot 1980 2022 all```, ```python .\scripts\scrape_stats_cli.py -adv 1980 2022 all```, and ```python .\scripts\scrape_teamrecords.py```.
4. Every day you want data, run the .\scripts\daily_data_script.py program to get the 2022 data.
5. Install and open ```DBeaver``` for your operating system. Have it open a connection to the database in this repository, after which you should import the files you scraped in step 3. Drop any outdated tables before import.
6. Import the 2022 data as well from ```\baseData\dailystats```. Steps 5 and 6 can likely be improved by a Python script that saves directly to a database. This is a future feature.
7. Run the ```allPlayers.sql``` and ```players2022.sql``` (or the ```_dbeaver```-suffixed) scripts to extract and transform the relevant data and save them to CSV files.
8. Load these files into Python and the models using ```python .\scripts\daily_modeling.py``` Follow the command line prompts to select files.
9. Your resulting file should be in the same path as you chose in Step 8. Open RStudio, set your data folder as your working directory and change any paths you need to change in the relevant functions. Like any other R function, load the libraries, copy the functions into the Console and run them, and then run your function.

```plot_predictions(year, month, day)``` - Plots the machine learning modeling output in a convenient-to-read form.

```automate_plotting("startDate", "endDate")``` - Runs plot predictions for every date between startDate and endDate, inclusive.

```plot_today()``` - Instead of running plot_predictions and manually entering in today's date, if you're just plotting today's data, run this.


Models
===========
**Currently implemented**
* [Support Vector Machine (SVM)](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
* [Random Forest (RF)](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
* [Multilayer perceptron (MLP)](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html), a feedforward artificial neural network
* [XGBoost](https://xgboost.readthedocs.io/en/stable/), a gradient boosting method

* Hyperparameter tuning

**To be implemented or displayed**
* Data checks to ensure proper data handling, providing confusion matrices and accuracy for cross-validation
* A time-lapse of these model outputs as players play more games
* Tableau dashboard of information

**Planned Improvements or Refinements**
* Considering inclusion/exclusion of predictors
* Smaller scale analysis using 538's RAPTOR, EPM, PIPM, or similar.

**Discarded Ideas**
* Naive Bayes Classifier: good classifier, but probability not particularly informative
* Stochastic Gradient Descent: data set not big enough to justify use over SVM
* k-Nearest Neighbors (kNN): Coded in but discarded, its probabilities emphasizes recall less than the other methods



Example Output
========
For example, the following figure shows the status of these players through 11/30/2021. We are still quite a ways away from the all-star or all-NBA selections (19-23 games into the season), but a lot of the players who we have come to expect to be yearly candidates for these spots have risen to expectations.

![allLeague Candidates](https://user-images.githubusercontent.com/78449574/144187461-5f5c0f2a-9eed-4a0d-a35e-7dfcd4c91f9c.png)

It is worth noting that all four of these models are being used as a classifier models and not as regressor models. That means these values are the probability of these player being classified as a 1 (receiving all-star or all-NBA recognition) vs. a 0.

Hyperparameter Tuning
===========
Hyperparameter tuning was conducted on the four models, as can be seen in the files ```MLPtuning.py / MLPgraphing.py```, ```RFtuning.py```, and within ```SVMmodeling.py``` in the scripts folder. A ```GridSearch``` was carried out for RF and MLP. 

Multilayer Perceptron Tuning
---------
For MLP, varied parameters included ```hidden_layer_sizes```, ```solver```, ```activation```, ```alpha```, and ```learning_rate```. 

Hidden layer sizes for the 7 input and 1 output node were varied between a single hidden layer of 1-10 nodes, inclusive, two hidden layers with various sizes, maxing out at (4,4), and three relatively small hidden layers, such as (1,2,1), (1,3,1), (2,2,2), etc. A [rule-of-thumb found on stats stackexchange](https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw) suggested that a single hidden layer of 4 nodes would be a good starting point, hence the other choices.

As for the other parameters, solver were initially varied between ```lbfgs``` (Gaussian) and ```adam```. ```sgd``` was initially considered but discarded because it provided suboptimal results upon validation. The ```learning_rate``` only applies to ```sgd``` models so it was left at default as well. Finally, the ```activation``` was testing between ```tanh``` and ```relu```, but difference in results between these two were minimal, so the default of ```relu``` was selected.

Random Forest Tuning
-------------
The main parameters tested for random forests were ```n_estimators```, ```max_depth``` and ```max_leaf_nodes```. The default values for these are ```n_estimators = 100``` awnd ```None``` for the other two. Another rule-of-thumb for ```n_estimators``` is the square root of the number of training set items, which was around 75. Through some quick testing, the defaults were all found to be more than sufficient for this analysis.
