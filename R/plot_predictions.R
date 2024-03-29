library(dplyr)
library(ggplot2)
library(matrixStats)
library(lubridate)

get_top_candidates <- function(date) {
  year <- substr(as_date(date), 1, 4)
  month <- substr(as_date(date), 6, 7)
  day <- substr(as_date(date), 9, 10)
  date_nospace <- paste(year, month, day, sep="")
  filename <- paste("stats_", date_nospace, "_modeled", sep="")
  folderName <- paste(year, "-", month, "-", day, "/", sep="")
  fullPath <- paste("~/GitHub/All-Star-Predictions/baseData/dailystats/", folderName, filename, ".csv", sep="")
  currstats <- read.csv(fullPath)

  df <- select(currstats, Player, RF, SVM, kNN, GBM, MLP, XGB)

  # Removed kNN because it is consistently lower than the other models.
  df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP, GBM, XGB)), na.rm = TRUE)
  df$SD <- rowSds(as.matrix(subset(df, select = c(RF, SVM, MLP, GBM, XGB))), na.rm = TRUE)
  topCandidates <- filter(df, Avg > 0.25)
  attach(topCandidates)
  topCandidates <- topCandidates[order(-Avg),]
  detach(topCandidates)

  return(topCandidates)
}

run_predictions <- function(date) {
  year <- substr(as_date(date), 1, 4)
  month <- substr(as_date(date), 6, 7)
  day <- substr(as_date(date), 9, 10)

  topCandidates <- get_top_candidates(date)

  saveFileName <- paste("~/GitHub/All-Star-Predictions/R/Graphs/Model Output ", year, month, day, ".png", sep="")

  plot_predictions(topCandidates, date, saveFlag = TRUE)
}



# Enter in yyyy-mm-dd as a string, e.g. "2021-12-10"
plot_predictions <- function(topCandidates, date, saveFlag)
{
  year <- substr(as_date(date), 1, 4)
  month <- substr(as_date(date), 6, 7)
  day <- substr(as_date(date), 9, 10)

  #dev.off()
  currPlot <- ggplot(data = topCandidates, aes(x = Player, y = RF)) +
    theme_bw() +
    ggtitle(paste("All-League Probabilities (", year, "-", month, "-", day, ")", sep = "")) +
    theme(axis.text.y = element_text(face = "bold")) +
    ylab("Model Probability") +
    xlab("") +
    scale_x_discrete(limits = rev(c(topCandidates$Player))) +
    scale_y_continuous(breaks = seq(0,1,0.1)) +
    coord_flip() +
    geom_point(aes(x = Player, y = RF, color = "RF"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = SVM, color = "SVM"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = MLP, color = "MLP"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = GBM, color = "GBM"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = XGB, color = "XGB"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = Avg, color = "Avg"), size = 3, alpha = 1) +
    scale_color_manual(values = c("RF" = "springgreen",
                                  "SVM" = "goldenrod",
                                  "MLP" = "royalblue4",
                                  "GBM" = "pink2",
                                  "XGB" = "maroon3",
                                  "Avg" = "gray24"))

  if(saveFlag == TRUE)
    ggsave(
      filename = paste("Model Output ", year, month, day, ".png", sep=""),
      plot = currPlot,
      device = "png",
      path = "~/GitHub/All-Star-Predictions/R/Graphs/",
      width = 12,
      height = 9.75,
      units = "in",
      dpi = 500,
    )

  print(currPlot)
  return(currPlot)

}


#today <- format(Sys.Date(), "%Y %b %d")
plot_today <- function() {
  today <- Sys.Date()

  run_predictions(today)
}

plot_today()
