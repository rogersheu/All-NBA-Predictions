library(dplyr)
library(ggplot2)
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
  topCandidates <- filter(df, Avg > 0.25)
  attach(topCandidates)
  topCandidates <- topCandidates[order(-Avg),]
  detach(topCandidates)
  
  
  saveFileName = paste("~/GitHub/All-Star-Predictions/R/Graphs/Model Output ", year, month, day, ".png", sep="")
  
  
  currPlot <- ggplot(topCandidates, aes(x=Player, y=RF)) + 
    theme_bw() + 
    theme(axis.text.y = element_text(face = "bold")) +
    ylab("Model Probability") +
    xlab("") + 
    scale_y_continuous(breaks=seq(0,1,0.1)) +
    scale_x_discrete(limits = rev(c(topCandidates$Player))) +
    coord_flip() +
    geom_point(aes(x=Player, y=RF, color = "RF"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
    geom_point(aes(x=Player, y=SVM, color = "SVM"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
    geom_point(aes(x=Player, y=kNN, color = "kNN"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
    geom_point(aes(x=Player, y=MLP, color = "MLP"), position = position_jitter(w=.1), size = 3, alpha = 0.25) +
    geom_point(aes(x=Player, y=XGBoost, color = "XGBoost"), position = position_jitter(w=.1), size = 3, alpha = 0.5) +
    geom_point(aes(x=Player, y=Avg, color = "Avg"), size = 3, alpha = 1) +
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


plot_predictions("2021", "12", "03")