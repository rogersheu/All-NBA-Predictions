# Predicting All-Star/All-NBA Selections

For Recruiters
-------
If you are here because you want to get an example of my work, please peruse the following files.

In ```/rogersheu/NBA-ML-Predictions/scripts/```:

**Web scraping**

* ```daily_data_scrape.py``` and ```scrape_stats_cli.py``` (BeautifulSoup, data cleaning, text manipulation and basic NLP, test cases, functions with arguments)
* ```get_player_birthdates.py``` (Scraping data and manipulating web elements with Selenium)

**Machine Learning**

Modeling
* ```daily_modeling.py``` (Runs the four models in the next bullet point)
* ```RFmodeling.py SVMmodeling.py MLPmodeling.py XGBoostmodeling.py``` (scikit-learn, model execution, called from ```daily_modeling.py```, some matplotlib)

Tuning (Training, Validating, Testing)
* ```RFtuning.py MLPtuning.py``` (scikit-learn, GridSearchCV to tune hyperparameters, train_test_split)
* ```MLPgraphing.py``` (scikit-learn, matplotlib of recall vs. precision)

**Code Management**

Helper Functions
* ```csv_functions.py``` (writes to CSV files, deletes a CSV file to ensure clean start)
* ```transfer_data.py``` (pandas and tkinter to pick paths/files from directory, includes quick data operations)

**Databases**

* Relational database of players: ```/rogersheu/NBA-ML-Predictions/baseData/allPlayerStats.db```
* SQL functions: ```/rogersheu/NBA-ML-Predictions/scripts/SQL/```
* ```players2022_dbeaver.sql``` (common table expressions, multiple joins, data filters via subqueries and LIMIT 1, aliases, and ensuring accuracy/readability of data using ROUND/CAST)

**Visualizations**

Under construction, both locally in R (locally referring to within this repository) and elsewhere in Tableau Public. Graphs can be shared upon request.


Objective/Motivation
===========
Using machine learning and deep learning models, identify players most likely to be selected onto either the NBA all-star team (halfway through the season) or an all-NBA team (at the end of the season). Inspiration and/or methodology from [here](https://www.reddit.com/r/nba/comments/bcdpls/oc_using_machine_learning_to_predict_the_2019_mvp/). Only the overarching information in that post was used. The code was written from scratch or sourced from unrelated analyses found online, especially scikit-learn's documentation.

Plenty of NBA aficionados try to predict who they think will be all-stars and all-NBA players. However, opinions vary widely between fans, and they often use any number of metrics (or lack thereof). People fall into various biases, including recency bias and letting their emotions cloud their better judgment. On the other hand, the human element is critical for accurate evaluation of performance, since while data collection is extensive, the big picture may still remain incomplete. In this project, I take inspiration from a previous attempt at this endeavor and make some improvements of my own. I hope to provide a statistical foundation upon which opinions can then be tweaked and crystallzied. I also wish to track each candidate's progress over time, since time is an important dimension to these analyses.


Installation/Instructions
===========
Prerequisites: ```Python 3.10```, ```sqlite3```, ```DBeaver```, ```R (RStudio)```

Scraping data (```Python 3.10```)
-------
1. In order to use this program, either ```Clone``` the repository or ```download the ZIP file```.
2. Windows instructions: Go into ```Command Prompt```, change directory to this repository's folder in the GitHub folder (not any of the subfolders) using ```cd <this repository's path>```.
3. Go into your virtualenv. Install any missing packages using ```pip install```.
4. Get the full historical data set (back to 1979-1980) by running ```python .\scripts\scrape_stats_cli.py -tot 1980 2022 all```, ```python .\scripts\scrape_stats_cli.py -adv 1980 2022 all```, and ```python .\scripts\scrape_teamrecords.py```. Warning: This script and the one in Step 5 use Structural Python Matching, which was introduced in Python 3.10. If you do not have Python 3.10, either update to it or change lines 152-163 in ```scrape_stats_cli.py``` to be a series of ```if-elif```.
5. Every day you want data, run the ```.\scripts\daily_data_script.py``` program to get the 2022 data. 

Database (```DBeaver```, ```SQLite3```)
--------
6. Install and open ```DBeaver``` for your operating system. Have it open a connection to the database ```allPlayerStats.db``` in this repository, after which you should import the files containing historical stats you scraped in step 4. Drop any outdated tables before import if they exist.
7. Import the 2022 data as well by importing from ```\baseData\dailystats```. Steps 6 and 7 can likely be improved by a Python script that saves directly to a database.
8. Run the ```allPlayers.sql``` and ```players2022_dbeaver.sql``` scripts, and ```table_modifiers_dbeaver.sql``` to extract and transform the relevant data and save them to CSV files. I personally like saving CSV files to the ```\baseData\dailystats\<date>``` folder under the name ```stats_${date}```.
9. (Optional) If you are running this on consecutive days, you can run the ```auxiliary_functions.sql``` to drop relevant tables and ```table_modifiers_dbeaver.sql``` to keep table names and column names consistent.

Machine Learning (```Python```, ```scikit-learn```)
---------
10. Load these files into Python and the models using ```python .\scripts\daily_modeling.py``` Follow the command line prompts.

Visualization (```RStudio```)
----------
11. Your resulting file should be in the same path as you chose in Step 8. Open RStudio, set your your working directory (I would recommend ```~/GitHub/All-Star-Predictions/All-Star-Predictions/R``` and change any paths you need to change in the relevant functions. 
12. Install and load the necessary libraries, copy the functions into the Console and run them, and then run your function. I would recommend ```plot_predictions``` and ```plot_predictions_line_graph```.

```plot_predictions(year, month, day)``` - Plots the machine learning modeling output in a convenient-to-read form.

```automate_plotting("startDate", "endDate")``` - Runs plot predictions for every date between startDate and endDate, inclusive.

```plot_today()``` - Instead of running plot_predictions and manually entering in today's date, if you're just plotting today's data, run this.

```plot_predictions_line_graph(startDate, endDate)``` and ```plot_Nplayers(startIndex, endIndex)``` - Creates a line graph time series across from the ```startDate``` to the ```endDate```.


Models
===========
**Currently implemented**
* [Support Vector Machine (SVM)](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
* [Random Forest (RF)](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
* [Multilayer perceptron (MLP)](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html), a feedforward artificial neural network
* [XGBoost](https://xgboost.readthedocs.io/en/stable/), a gradient boosting method

* Hyperparameter tuning

**To be implemented or displayed**
* Tableau dashboard of information

**Planned Improvements or Refinements**
* Considering inclusion/exclusion of predictors
* Smaller scale analysis using 538's RAPTOR, EPM, PIPM, or similar.

**Discarded Ideas**
* Naive Bayes Classifier: good classifier, but probability not particularly informative
* Stochastic Gradient Descent: data set not big enough to justify use over SVM
* k-Nearest Neighbors (kNN): Coded in but discarded, its probabilities emphasizes recall less than the other methods

Methodology
========
Web Scraping
--------
Explanation under construction


Feature Selection: Preemptively Identifying Potential Overfitting
--------
Features were chosen in an easily accessible and easily calculable way.

Feature requirements:

* Easily accessible. Provide as big of a sample size as possible. Advanced analytics, i.e., PIPM, RAPM, RAPTOR, EPM, LEBRON, etc., only have data since the 2000's, if not even more recent. For some of these, it's because Tracking data only became more sophisticated in the 21st century.
* Rate metrics only. Because these metrics would be actively updated partway through the season, it makes no sense to compare these to other players' full season stats. Other options included using per 36 minute numbers or per 75 possession numbers. However, I ended up going with per game values. These can be made more volatile if a player has high game-to-game variance (i.e., foul trouble, playing fewer minutes in blowouts, etc.), but voters take most stock in per game numbers.
* Still, these statistics must be pace adjustable. The pace of play in the NBA has changed a decent amount across the decades. While some of the models eventually normalize the data, pace should still be adjusted to account for high or low volume environments. These pace adjustments are made in SQLite.
* Minimal collinearity. Other measures such as Value Over Replacement Player (VORP), Box Plus Minus (BPM), and Win Shares (WS) were considered, but had high correlation (r^2 > 0.7) with WS/48, so they were discarded for the models.
* Use as few, but as descriptive metrics as possible. Other similar models excised steals/blocks, since these defensive statistics can be misleading. An argument can also be made to include team seeding. However, I believed that steals/blocks add a new dimension to the analysis that voters do take into account that are not already covered by other features.

The statistics used were the following.

| Features | 
| --- |
| Points Per Game (PPG) |
| Rebounds Per Game (RPG) |
| Assists Per Game (APG) |
| Steals + Blocks Per Game (SBPG) |
| True Shooting percentage (TS%) |
| Win Shares per 48 minutes (WS/48) |
| Team Winning Percentage (Perc) |

Predictor: I call it ```All-League Selection```, which is the intersection of All-Star picks and All-NBA picks. This makes sure some players who made one or the other are not excluded. 24 All-Star are picked every season (with possibility a few more with injury replacements), while 15 players are selected for All-NBA. Most of the time, All-NBA players are selected as All-Stars in the same season, while the opposite occurs less often (e.g., Rudy Gobert in 2017 and 2019). Soemtimes, this discrepancy occurs because of positional limits. All-Stars have since shifted to a frontcourt/backcourt voting approach, while All-NBA selections remain on the guards/forwards/centers categories. Other times, it's a result of the relevant schedule period. All-Stars are picked around halfway into the season, so players who get injured or falter later on can miss the All-NBA teams. Alternatively, players who outperform their first half can elevate into an All-NBA pick if others fade.

Example Output
========
Example #1, plot_predictions.R
--------
For example, the following figure shows the status of these players through 12/21/2021. We are still quite a ways away from the all-star or all-NBA selections (almost 30 games into the season), but a lot of the players who we have come to expect to be yearly candidates for these spots have risen to expectations.

<p align="center" width="100%">
    <img width="75%" src="https://user-images.githubusercontent.com/78449574/147544645-a8bdab79-d8da-407b-8a7a-f857308c12f9.png">
</p>


It is worth noting that all four of these models are being used as a classifier models and not as regressor models. That means these values are the probability of these player being classified as a 1 (receiving all-star or all-NBA recognition) vs. a 0.

Example #2, plot_predictions_line_graph.R
--------
Here's another example, showing the likelihood of being classified as an all-League players in 2022 over time. They're grouped in 5's, from the highest probability to the lowest down to a minimum threshold.

For example, here are the trends for the 24st-28th highest players as of 12/27/2021.

<p align="center" width="100%">
    <img width="75%" src="https://user-images.githubusercontent.com/78449574/147544678-f48e0933-ea62-4897-8e42-63d41bf24ee2.png">
</p>


Hyperparameter Tuning
===========
Hyperparameter tuning was conducted on the four models, as can be seen in the files ```MLPtuning.py / MLPgraphing.py```, ```RFtuning.py```, and within ```SVMmodeling.py``` in the scripts folder. A ```GridSearch``` was carried out for RF and MLP. 

Random Forest & Random Forest Tuning
-------------
Random Forest modeling involves the randomized generation of many decision trees, which sorts objects between two outcomes based on where comparisons between the features in the training set are classified.

The main parameters tested for random forests were ```n_estimators```, ```max_depth``` and ```max_leaf_nodes```. The default values for these are ```n_estimators = 100``` and ```None``` for the other two. Another rule-of-thumb for ```n_estimators``` is the square root of the number of training set items, which was around 75. Through some quick testing, the defaults were all found to be more than sufficient for this analysis.

Multilayer Perceptron & Multilayer Perceptron Tuning
---------
Multilayer perceptron is a feedforward artificial neural network. The one used here is a "vanilla" neural network, indicating that it has one hidden layer. MLPs have at least three layers: an input layer (here, 7 features: PPG, RPG, APG, SBPG, TS%, WS48, and Team Winning Percentage), one or more hidden layers (here, a single layer of 4 nodes), and an output layer (here, a single node that's either on or off).

For MLP, varied parameters included ```hidden_layer_sizes```, ```solver```, ```activation```, ```alpha```, and ```learning_rate```. 

Hidden layer sizes for the 7 input and 1 output node were varied between a single hidden layer of 1-10 nodes, inclusive, two hidden layers with various sizes, maxing out at (4,4), and three relatively small hidden layers, such as (1,2,1), (1,3,1), (2,2,2), etc. A [rule-of-thumb found on stats stackexchange](https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw) suggested that a single hidden layer of 4 nodes would be a good starting point, hence the other choices.

As for the other parameters, solver was initially varied between ```lbfgs``` (Gaussian) and ```adam```. ```sgd``` was initially considered but discarded because it provided suboptimal results upon validation. The ```learning_rate``` only applies to ```sgd``` models so it was left at default as well. Finally, the ```activation``` was testing between ```tanh``` and ```relu```, but difference in results between these two were minimal, so the default of ```relu``` was selected.

XGBoost Tuning
--------
To be implemented.
