library(dplyr)
library(ggplot2)
library(reshape2)
library(tibble)
library(janitor)
library(stringr)
library(directlabels)
library(scales)

plot_predictions_line_graph <- function(startDate, endDate) { #YYYY-MM-DD format
  ### reshape2 provides a pretty big warning with the melt function...
  options(warn=-1)
  
  # Need to initialize these data frames or else you'll get an error later
  # when you try to put data into them.
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
    
    # Only filtered out practically irrelevant players
    topCandidates <- filter(df, Avg >= 0) # Change this to 0.25 if needed
    
    ### Tried using lapply on these next few, but was not successful.
    # Isolates data
    RFonly <- select(topCandidates, Player, RF)
    SVMonly <- select(topCandidates, Player, SVM)
    MLPonly <- select(topCandidates, Player, MLP)
    XGBoostonly <- select(topCandidates, Player, XGBoost)
    Avgonly <- select(topCandidates, Player, Avg)
    
    # Combines all such data
    df_RF <- merge(df_RF, RFonly, by = "Player", all = TRUE)
    df_SVM <- merge(df_SVM, SVMonly, by = "Player", all = TRUE)
    df_MLP <- merge(df_MLP, MLPonly, by = "Player", all = TRUE)
    df_XGBoost <- merge(df_XGBoost, XGBoostonly, by = "Player", all = TRUE)
    df_Avg <- merge(df_Avg, Avgonly, by = "Player", all = TRUE)
    
    # Renames columns to dates
    names(df_RF)[names(df_RF) == 'RF'] <- date_dash
    names(df_SVM)[names(df_SVM) == 'SVM'] <- date_dash
    names(df_MLP)[names(df_MLP) == 'MLP'] <- date_dash
    names(df_XGBoost)[names(df_XGBoost) == 'XGBoost'] <- date_dash
    names(df_Avg)[names(df_Avg) == 'Avg'] <- date_dash
  }
  
  topCandidates <<- topCandidates
  
  # Removes first column
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
  
  # Send to global environment
  df_RF <<- df_RF
  df_SVM <<- df_SVM
  df_MLP <<- df_MLP
  df_XGBoost <<- df_XGBoost
  df_Avg <<- df_Avg
  
  
  ### Choice between filtering by average probability
  #bestAvg <- filter(df_Avg, Avg >= .1)
  
  ### or filtering by highest probability throughout time interval indicated
  bestAvg <- filter(df_Avg, rowMaxs(as.matrix(df_Avg[,2:17])) > 0.5)
  ### Sort by Average
  #bestAvg <- bestAvg[order(bestAvg[,-Avg]),]
  ###
  
  ### Sort by most recent date
  bestAvg <- bestAvg[order(bestAvg[,ncol(bestAvg)], decreasing = TRUE),]
  
  ### Removes Average column, only used to filter.
  bestAvg <- subset(bestAvg, select = -c(Avg))
  
  ### Sends bestAvg to the global environment
  bestAvg <<- bestAvg

  ### Plot gets messy if too many players are shown at once
  increment <- 5
  fileIndex <- 1
  for(startIndex in seq(2, nrow(bestAvg), increment)) {
    endIndex <- startIndex + 4
    ### Plot is awkward if only one or two players is tacked on at the end
    if(endIndex > nrow(bestAvg) - increment) {
      endIndex = nrow(bestAvg)
    }
    plot_fiveplayers(startIndex, endIndex, fileIndex)
    if(endIndex > nrow(bestAvg) - increment) {
      break
    }
    fileIndex <= fileIndex+1
  }
  
}