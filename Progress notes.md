Notes
=======

Outlier Stat Lines
------------
Is outlier detection an option or are SVM and similar processes sufficiently capturing outlier behavior?

Multivariate outlier detection
* https://stats.stackexchange.com/questions/213/what-is-the-best-way-to-identify-outliers-in-multivariate-data

Would need to specify some sort of minimum bound so we ensure we're looking for maxima and not minima. Though given the log-normal (?) nature of NBA statistics, this may not be necessary.

Progress: I'm thinking we're far enough along into machine learning that pure outlier detection is not necessary.


Player Birthdays for more accurate ages
-------------
Objective: Use player codes to grab birth dates to get a more accurate age-weighted distribution of minutes

Progress: This code, using Selenium, can be found at rogersheu/NBA-ML-Predictions/scripts/get_player_birthdates.py
