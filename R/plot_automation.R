library(lubridate)

automate_plotting <- function(startDate, endDate) { #YYYY-MM-DD format
  for(date in seq(as_date(startDate), as_date(endDate), by = "day")) {
    plot_predictions(substr(as_date(date), 1, 4), substr(as_date(date), 6, 7), substr(as_date(date), 9, 10))
  }
}


#automate_plotting("2021-12-07", "2021-12-08")




#today <- format(Sys.Date(), "%Y %b %d")
plot_today <- function() {
  today <- Sys.Date()
  year <- toString(year(today))
  month <- toString(month(today))
  day <- toString(day(today))
  if (month(today) < 10) {
    month <- paste("0", month, sep = "")
  }
  if (day(today) < 10) {
    day <- paste("0", day, sep = "")
  }
  run_predictions(today)
}