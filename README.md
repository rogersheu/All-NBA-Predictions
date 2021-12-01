# AllLeague-NBA-Predictions

Use
===========
Under construction.

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
* Tableau dashboard of information

Planned Improvements or Refinements
* Implementation of other machine learning methods
* Considering inclusion/exclusion of predictors
* Smaller scale analysis using 538's RAPTOR, EPM, PIPM, or similar.



For example, the following figure shows the status of these players through 11/30/2021. We are still quite a ways away from the all-star or all-NBA selections (17-20 games into the season), but a lot of the players who we have come to expect to be yearly candidates for these spots have risen to expectations.

![allLeague Candidates](https://user-images.githubusercontent.com/78449574/144187461-5f5c0f2a-9eed-4a0d-a35e-7dfcd4c91f9c.png)

It is worth noting that all four of these models are classifier models and not regressor models. That means these values are the probability of these player being classified as a 1 (receiving all-star or all-NBA recognition) vs. a 0.
