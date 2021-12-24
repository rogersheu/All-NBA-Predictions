library(dplyr)

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
    fileName <- paste("stats_", date, "_modeled", sep="")
    folderName <- paste(year, "-", month, "-", day, "/", sep="")
    fullPath <- paste("~/GitHub/All-Star-Predictions/baseData/dailystats/", folderName, fileName, ".csv", sep="")
    temp_stats <- read.csv(fullPath)
    
    df <- select(temp_stats, Player, RF, SVM, kNN, MLP, XGBoost, Avg)
    df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP, XGBoost)), na.rm = TRUE) # Removed kNN because it is consistently lower than the other models.
    
    topCandidates <- filter(df, Avg >= 0) # Change this to 0.25 if needed
    
    #attach(topCandidates)
    #topCandidates <- topCandidates[order(-Avg),]
    #detach(topCandidates)
    
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
    
    names(df_RF)[names(df_RF) == 'RF'] <- date
    names(df_SVM)[names(df_SVM) == 'SVM'] <- date
    names(df_MLP)[names(df_MLP) == 'MLP'] <- date
    names(df_XGBoost)[names(df_XGBoost) == 'XGBoost'] <- date
    names(df_Avg)[names(df_Avg) == 'Avg'] <- date
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
  
  bestAvg <- filter(df_Avg, Avg >= .05)
  attach(bestAvg)
  bestAvg <- bestAvg[order(-Avg),]
  detach(bestAvg)
  
  
}