library(dplyr)
library(ggplot2)
library(matrixStats)
library(lubridate)

# Enter in yyyy, mm, dd format as STRINGS
plot_predictions <- function(year, month, day) 
{
  date <- paste(year, month, day, sep="")
  filename <- paste("stats_", date, "_modeled", sep="")
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
  
  
  saveFileName = paste("~/GitHub/All-Star-Predictions/R/Graphs/Model Output ", year, month, day, ".png", sep="")
  
  #dev.off()
  
  currPlot <- ggplot(topCandidates, aes(x = Player, y = RF)) + 
    theme_bw() + 
    ggtitle(paste("All-League Classifications Predictions (", year, "-", month, "-", day, ")", sep = "")) + 
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
  
}

