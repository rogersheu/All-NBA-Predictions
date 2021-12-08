library(dplyr)
library(ggplot2)
library(matrixStats)
library(lubridate)

plot_predictions <- function(year, month, day) # Enter in yyyy, mm, dd format as STRINGS
{
  date <- paste(year, month, day, sep="")
  filename <- paste("stats_", date, "_modeled", sep="")
  folderName <- paste(year, "-", month, "-", day, "/", sep="")
  fullPath <- paste("~/GitHub/All-Star-Predictions/baseData/dailystats/", folderName, filename, ".csv", sep="")
  currstats <- read.csv(fullPath)

  
  df <- select(currstats, Player, RF, SVM, kNN, MLP, XGBoost)
  
  df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP, XGBoost)), na.rm = TRUE) # Removed kNN because it is consistently lower than the other models.
  # Perhaps that's indicating that I need to tune the hyperparameters on the other models?
  df$SD <- rowSds(as.matrix(subset(df, select = c(RF, SVM, MLP, XGBoost))), na.rm = TRUE) 
  topCandidates <- filter(df, Avg > 0.25)
  attach(topCandidates)
  topCandidates <- topCandidates[order(-Avg),]
  detach(topCandidates)
  
  
  saveFileName = paste("~/GitHub/All-Star-Predictions/R/Graphs/Model Output ", year, month, day, ".png", sep="")
  
  
  currPlot <- ggplot(topCandidates, aes(x = Player, y = RF)) + 
    theme_bw() + 
    theme(axis.text.y = element_text(face = "bold")) +
    ylab("Model Probability") +
    xlab("") + 
    scale_x_discrete(limits = rev(c(topCandidates$Player))) +
    scale_y_continuous(breaks = seq(0,1,0.1)) +
    #coord_cartesian(ylim = c(0,1)) +
    coord_flip() +
    geom_point(aes(x = Player, y = RF, color = "RF"), position = position_jitter(w=.1), size = 3, alpha = 0.1) + 
    geom_point(aes(x = Player, y = SVM, color = "SVM"), position = position_jitter(w=.1), size = 3, alpha = 0.5) + 
    geom_point(aes(x = Player, y = kNN, color = "kNN"), position = position_jitter(w=.1), size = 3, alpha = 0.5) + 
    geom_point(aes(x = Player, y = MLP, color = "MLP"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x = Player, y = XGBoost, color = "XGBoost"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_errorbar(aes(ymin = Avg - SD, ymax = Avg + SD, color = "gray"), width = .5, alpha = 0.5) + 
    geom_point(aes(x = Player, y = Avg, color = "Avg"), size = 3, alpha = 1) +
    scale_color_manual(values = c("RF" = "springgreen", "SVM" = "goldenrod", "kNN" = "red4", "MLP" = "royalblue", 
                                  "XGBoost" = "hotpink", "Avg" = "gray24"))

  ggsave(
    filename = paste("Model Output ", year, month, day, ".png", sep=""),
    plot = currPlot,
    device = "png", 
    path = "~/GitHub/All-Star-Predictions/R/Graphs/",
    # width = 12,
    # height = 9.75,
    # units = "in"
  )
  
  currPlot
  
}


#today <- format(Sys.Date(), "%Y %b %d")
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
plot_predictions(year, month, day)