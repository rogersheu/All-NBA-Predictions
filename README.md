# AllLeague-NBA-Predictions

Installation/Instructions
===========
1. In order to use this program, either ```Clone``` the repository or ```download the ZIP file```. 
2. Go into python, change directory to the GitHub's folder (not any of the subfolder).
3. Get the full data by running ```python .\scripts\scrape_stats_cli.py -tot 1980 2022 all```, ```python .\scripts\scrape_stats_cli.py -adv 1980 2022 all```, and ```python .\scripts\scrape_teamrecords.py```.
4. Then, run the .\scripts\daily_data_script.py program to get the 2022 data.
5. Install and open ```DBeaver```. Have it open a connection to the database, after which you should import three files you should have gotten in step 3. Drop any outdated tables before import.
6. Import the 2022 data as well from ```\baseData\dailystats```. Steps 5 and 6 can likely be improved by a Python script that saves directly to a database. This is a future feature.
7. Run the ```allPlayers.sql``` and ```players2022.sql``` scripts to extract and transform the relevant data and save them to CSV files.
8. Load these files into Python and the models using ```python .\scripts\daily_modeling.py``` Follow the command line prompts to select files.
9. Your resulting file should be in the same path as you chose in Step 8.

Objective
===========
Using machine learning and deep learning models, identify players most likely to be selected onto either the NBA all-star team (halfway through the season) or an all-NBA team (at the end of the season). Inspiration and/or methodology from [here](https://www.reddit.com/r/nba/comments/bcdpls/oc_using_machine_learning_to_predict_the_2019_mvp/). Only the overarching information in that post was used. The code was written from scratch or sourced from unrelated analyses found online.

Models
===========
Currently implemented
* Support Vector Machine (SVM)
* Random Forest (RF)
* k-Nearest Neighbors (kNN)
* Multilayer perceptron (MLP), a feedforward artificial neural network

To be implemented or displayed
* Data checks to ensure proper data handling, providing confusion matrices and accuracy for cross-validation
* Naive Bayes Classifier, Stochastic Gradient Descent
* Tableau dashboard of information

Planned Improvements or Refinements
* Implementation of other machine learning methods
* Considering inclusion/exclusion of predictors
* Smaller scale analysis using 538's RAPTOR, EPM, PIPM, or similar.



For example, the following figure shows the status of these players through 11/30/2021. We are still quite a ways away from the all-star or all-NBA selections (17-20 games into the season), but a lot of the players who we have come to expect to be yearly candidates for these spots have risen to expectations.

![allLeague Candidates](https://user-images.githubusercontent.com/78449574/144187461-5f5c0f2a-9eed-4a0d-a35e-7dfcd4c91f9c.png)

It is worth noting that all four of these models are classifier models and not regressor models. That means these values are the probability of these player being classified as a 1 (receiving all-star or all-NBA recognition) vs. a 0.
