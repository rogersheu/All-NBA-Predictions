library(lubridate)

automate_plotting <- function(startDate, endDate) { #YYYY-MM-DD format
  for(date in seq(as_date(startDate), as_date(endDate), by = "day")) {
    run_predictions(date)
  }
}


#automate_plotting("2021-12-07", "2021-12-08")

date_parse <- function(date) {
  year <- toString(year(date))
  month <- toString(month(date))
  day <- toString(day(date))
  if (month(date) < 10) {
    month <- paste("0", month, sep = "")
  }
  if (day(date) < 10) {
    day <- paste("0", day, sep = "")
  }
}
