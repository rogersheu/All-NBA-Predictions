library(dplyr)
library(ggplot2)
library(reshape2)
library(tibble)
library(janitor)
library(stringr)

plot_predictions_line_graph <- function(startDate, endDate) { #YYYY-MM-DD format
  df_RF <- data.frame(Player = "")
  df_SVM <- data.frame(Player = "")
  df_MLP <- data.frame(Player = "")
  df_XGBoost <- data.frame(Player = "")
  df_Avg <- data.frame(Player = "")
  for(date in seq(as_date(startDate), as_date(endDate), by = "day")) {
    year <- substr(as_date(date), 1, 4)
    month <- substr(as_date(date), 6, 7)
    day <- substr(as_date(date), 9, 10)
    date <- paste(year, month, day, sep="")
    date_dash <- paste(year, month, day, sep="-")
    fileName <- paste("stats_", date, "_modeled", sep="")
    folderName <- paste(year, "-", month, "-", day, "/", sep="")
    fullPath <- paste("~/GitHub/All-Star-Predictions/baseData/dailystats/", folderName, fileName, ".csv", sep="")
    temp_stats <- read.csv(fullPath)
    
    df <- select(temp_stats, Player, RF, SVM, kNN, MLP, XGBoost, Avg)
    df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP, XGBoost)), na.rm = TRUE) # Removed kNN because it is consistently lower than the other models.
    
    topCandidates <- filter(df, Avg >= 0) # Change this to 0.25 if needed
    
    RFonly <- select(topCandidates, Player, RF)
    SVMonly <- select(topCandidates, Player, SVM)
    MLPonly <- select(topCandidates, Player, MLP)
    XGBoostonly <- select(topCandidates, Player, XGBoost)
    Avgonly <- select(topCandidates, Player, Avg)
    
    
    df_RF <- merge(df_RF, RFonly, by = "Player", all = TRUE)
    df_SVM <- merge(df_SVM, SVMonly, by = "Player", all = TRUE)
    df_MLP <- merge(df_MLP, MLPonly, by = "Player", all = TRUE)
    df_XGBoost <- merge(df_XGBoost, XGBoostonly, by = "Player", all = TRUE)
    df_Avg <- merge(df_Avg, Avgonly, by = "Player", all = TRUE)
    
    names(df_RF)[names(df_RF) == 'RF'] <- date_dash
    names(df_SVM)[names(df_SVM) == 'SVM'] <- date_dash
    names(df_MLP)[names(df_MLP) == 'MLP'] <- date_dash
    names(df_XGBoost)[names(df_XGBoost) == 'XGBoost'] <- date_dash
    names(df_Avg)[names(df_Avg) == 'Avg'] <- date_dash
  }
    
  df_RF <- df_RF[-1,]
  df_SVM <- df_SVM[-1,]
  df_MLP <- df_MLP[-1,]
  df_XGBoost <- df_XGBoost[-1,]
  df_Avg <- df_Avg[-1,]
  
  df_RF$Avg <- rowMeans(subset(df_RF, select = c(-Player)), na.rm = TRUE)
  df_SVM$Avg <- rowMeans(subset(df_SVM, select = c(-Player)), na.rm = TRUE)
  df_MLP$Avg <- rowMeans(subset(df_MLP, select = c(-Player)), na.rm = TRUE)
  df_XGBoost$Avg <- rowMeans(subset(df_XGBoost, select = c(-Player)), na.rm = TRUE)
  df_Avg$Avg <- rowMeans(subset(df_Avg, select = c(-Player)), na.rm = TRUE)
  
  df_RF <<- df_RF
  df_SVM <<- df_SVM
  df_MLP <<- df_MLP
  df_XGBoost <<- df_XGBoost
  df_Avg <<- df_Avg
  
  #bestAvg <- filter(df_Avg, Avg >= .05)
  bestAvg <- filter(df_Avg, rowMaxs(as.matrix(df_Avg[,2:17])) > 0.5)
  attach(bestAvg)
  bestAvg <- bestAvg[order(-Avg),]
  detach(bestAvg)
  
  bestAvg <<- bestAvg
  
  bestAvg_noAvg <- subset(bestAvg, select = -c(Avg))
  
  bestAvgs <- bestAvg_noAvg
  playernames <- bestAvgs[,1]
  bestAvgs <- bestAvgs[,-1]
  bestAvgs <- data.frame(t(bestAvgs))
  playernames <- c('Date', playernames)
  bestAvgs <- tibble::rownames_to_column(data.frame(bestAvgs), "Date")
  bestAvgs$Date <- as.Date(bestAvgs$Date)
  playernames <- str_replace_all(playernames, " ", "_")
  playernames <- str_replace_all(playernames, "'", "")
  playernames <- str_replace_all(playernames, "-", "")
  colnames(bestAvgs) <- playernames
  currplot <- ggplot(data = bestAvgs, aes(x = Date, y = 'Giannis_Antetokounmpo', group = 1)) + theme_bw() + ylim(0,1) + scale_x_date(date_breaks = "1 week")
  
  
  for (col in 2:ncol(bestAvgs)) {
    currPlayer <- colnames(bestAvgs)[col]
    currplot <- currplot + geom_line(aes_string(x = 'Date', y = currPlayer, group = 1))# + geom_point(aes_string(x = 'Date', y = currPlayer, group = 1))
  }
  
  currplot
}