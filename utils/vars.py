from datetime import datetime

curr_month = datetime.now().month
curr_year = datetime.now().year

curr_season = curr_year if curr_month < 10 else (curr_year + 1)
curr_season_str = str(curr_season)
