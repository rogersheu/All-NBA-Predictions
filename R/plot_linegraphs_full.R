library(directlabels)
library(scales)
library(RColorBrewer)
library(reshape2)
library(stats)
library(dplyr)
library(ggplot2)
library(tibble)
library(janitor)
library(stringr)
library(lubridate)
library(matrixStats)

#### REQUIRES INITIALIZATION, ESPECIALLY FOR TEAMCOLORS

processing_predictions <- function(startDate, endDate) { #YYYY-MM-DD format
  ### reshape2 provides a pretty big warning with the melt function...
  options(warn=-1)
  
  # Need to initialize these data frames or else you'll get an error later
  # when you try to put data into them.
  df_RF <- data.frame(Player = "")
  df_SVM <- data.frame(Player = "")
  df_MLP <- data.frame(Player = "")
  df_GBM <- data.frame(Player = "")
  df_XGB <- data.frame(Player = "")
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
    
    df <- select(temp_stats, Player, RF, SVM, kNN, MLP, GBM, XGB, Avg)
    df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP, GBM, XGB)), na.rm = TRUE) # Removed kNN because it is consistently lower than the other models.
    
    # Only filtered out practically irrelevant players
    topCandidates <- filter(df, Avg >= 0) # Change this to 0.25 if needed
    
    ### Tried using lapply on these next few, but was not successful.
    # Isolates data
    RFonly <- select(topCandidates, Player, RF)
    SVMonly <- select(topCandidates, Player, SVM)
    MLPonly <- select(topCandidates, Player, MLP)
    GBMonly <- select(topCandidates, Player, GBM)
    XGBonly <- select(topCandidates, Player, XGB)
    Avgonly <- select(topCandidates, Player, Avg)
    
    # Combines all such data
    df_RF <- merge(df_RF, RFonly, by = "Player", all = TRUE)
    df_SVM <- merge(df_SVM, SVMonly, by = "Player", all = TRUE)
    df_MLP <- merge(df_MLP, MLPonly, by = "Player", all = TRUE)
    df_GBM <- merge(df_GBM, GBMonly, by = "Player", all = TRUE)
    df_XGB <- merge(df_XGB, XGBonly, by = "Player", all = TRUE)
    df_Avg <- merge(df_Avg, Avgonly, by = "Player", all = TRUE)
    
    # Renames columns to dates
    names(df_RF)[names(df_RF) == 'RF'] <- date_dash
    names(df_SVM)[names(df_SVM) == 'SVM'] <- date_dash
    names(df_MLP)[names(df_MLP) == 'MLP'] <- date_dash
    names(df_GBM)[names(df_GBM) == 'GBM'] <- date_dash
    names(df_XGB)[names(df_XGB) == 'XGB'] <- date_dash
    names(df_Avg)[names(df_Avg) == 'Avg'] <- date_dash
  }
  
  topCandidates <<- topCandidates
  
  # Removes first column
  df_RF <- df_RF[-1,]
  df_SVM <- df_SVM[-1,]
  df_MLP <- df_MLP[-1,]
  df_GBM <- df_GBM[-1,]
  df_XGB <- df_XGB[-1,]
  df_Avg <- df_Avg[-1,]
  
  df_RF$Avg <- rowMeans(subset(df_RF, select = c(-Player)), na.rm = TRUE)
  df_SVM$Avg <- rowMeans(subset(df_SVM, select = c(-Player)), na.rm = TRUE)
  df_MLP$Avg <- rowMeans(subset(df_MLP, select = c(-Player)), na.rm = TRUE)
  df_GBM$Avg <- rowMeans(subset(df_GBM, select = c(-Player)), na.rm = TRUE)
  df_XGB$Avg <- rowMeans(subset(df_XGB, select = c(-Player)), na.rm = TRUE)
  df_Avg$Avg <- rowMeans(subset(df_Avg, select = c(-Player)), na.rm = TRUE)
  
  # Send to global environment
  # df_RF <<- df_RF
  # df_SVM <<- df_SVM
  # df_MLP <<- df_MLP
  # df_GBM <<- df_GBM
  # df_XGB <<- df_XGB
  # df_Avg <<- df_Avg
  
  
  ### Filtering by average probability
  # bestAvg <- filter(df_Avg, df_Avg[ncol(df_Avg)] >= .25)
  ###
  
  ### Filter by highest probability throughout time interval indicated
  # bestAvg <- filter(df_Avg, rowMaxs(as.matrix(df_Avg[,2:ncol(df_Avg)])) > 0.5)
  ###
  
  ### Sort by Average
  # bestAvg <- bestAvg[order(bestAvg[,-Avg]),]
  ###
  
  ### Filter by most recent probability
  bestAvg <- filter(df_Avg, df_Avg[ncol(df_Avg)-1] >= .25)
  ###
  
  ### Removes Average column, only used to filter.
  bestAvg <- subset(bestAvg, select = -c(Avg))
  
  ### Sort by most recent date
  bestAvg <- bestAvg[order(bestAvg[,ncol(bestAvg)], decreasing = TRUE),]
  
  ### Sends bestAvg to the global environment, for testing purposes
  bestAvg <<- bestAvg
  
  return(bestAvg)
  
}

plot_Nplayers <- function(data, startIndex, endIndex, endDate, saveFlag) {
  # Preparation for melt
  data_subset <- data[startIndex:endIndex,]
  
  # Melt, converts a data.frame from rows of players and columns as dates to:
  # | Player | variable (Dates) | value (Probabilities) |
  melted_players <- melt(data_subset, id='Player')
  
  # Creates a color vector, which is then saved to the melt data frame
  col_vector <- rep(NA, nrow(melted_players))
  melted_names <- melted_players[,1]
  for(index in 1:nrow(melted_players)) {
    currName <- melted_names[index]
    teamCode <- players2022$Tm[which(players2022$Player == currName)]
    currColor <- teamcolors$Color[which(teamcolors$Abbrev == teamCode)]
    col_vector[index] <- currColor
  }
  col_vector <<- col_vector
  melted_players['color'] <- col_vector
  
  
  # Converts player names from Firstname Lastname to F. Lastname
  player_names <- melted_players['Player']
  for(i in 1:nrow(player_names)) {
    player_names[i,1] <- convert_name(player_names[i,1])
  }
  melted_players['Player'] <- player_names
  
  melted_players[melted_players == "G. Antetokounmpo"] <- "Giannis"
  melted_players[melted_players == "S. Gilgeous-Alexander"] <- "SGA"
  
  #melted_players['Player'][melted_players['Player'] == "Giannis Antetokounmpo"] <- "Giannis"
  
  # Sends to global environment for inspection if needed.
  melted_players <<- melted_players
  
  # Adjusts x-axis to be further out to accommodate directlabels
  lastDate <- melted_players[nrow(melted_players),2]
  range <-  c(as.Date("2021-12-01") - 5, as.Date(endDate) + 5)
  
  lineplot <- ggplot(data=melted_players, aes(x=as.Date(variable), y=value, group=Player)) +
    geom_line(size=0.75, color = melted_players$color, group=melted_players$Player) + 
    geom_point(size=2, color = melted_players$color, group=melted_players$Player) +
    theme_bw() + # Removes gray
    theme(panel.grid.minor.x = element_blank()) + # no minor axis lines
    theme(panel.grid.minor.y = element_blank()) +
    theme(legend.position="none") + # no legend
    xlab("") + 
    ylab("Ensemble Average Probability") +
    theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1, size = 12)) +
    theme(axis.title.y = element_text(size = 16)) + 
    theme(axis.text.y = element_text(size = 14)) + 
    scale_x_date(date_breaks = "3 days", limits = range) + # Major axis (x) every three days, limits as set above
    scale_y_continuous(breaks = seq(0, 1, 0.05)) + 
    #scale_y_continuous(expand = expansion(mult = .1), breaks = seq(0, 1, 0.05)) + # If the y axis needs expanding
    geom_dl(aes(label = Player), color = melted_players$color, group=melted_players$Player, method = list(dl.trans(x = x + 0.2), "last.bumpup", cex = 1)) +
    geom_dl(aes(label = Player), color = melted_players$color, group=melted_players$Player, method = list(dl.trans(x = x - 0.2), "first.bumpup", cex = 1))
  
  #These global assignments are for sanity checking and could just as easily be removed.
  lineplot <<- lineplot 
  print(lineplot)
  
  if(saveFlag == 1) {
    ggsave(
      filename = paste("Top ", startIndex, "-", endIndex, " players.png", sep=""),
      #filename = paste("All-League Probability - ", data_subset[1, 1], ".png", sep=""),
      plot = lineplot,
      device = "png",
      path = paste("~/GitHub/All-Star-Predictions/R/Graphs/lineplots/", endDate, sep=""),
      width = 12,
      height = 9,
      units = "in",
      dpi = 500,
    )
  }
}

plot_predictions_clusters <- function(startDate, endDate) {
  
  data <- processing_predictions(startDate, endDate)
  
  cluster_sizes <- cluster_recent(data)
  startIndex <- 1
  for(i in 1:length(cluster_sizes)) {
    endIndex <- startIndex + (cluster_sizes[i] - 1)
    plot_Nplayers(data, startIndex, endIndex, endDate, 1)
    startIndex <- endIndex + 1
  }
}

cluster_recent <- function(data) {
  temp <- data
  data <- filter(temp, !is.na(temp[,ncol(temp)]))
  mostrecent <- data[c(1, ncol(data))] # Names and prob
  num_clusters <- round (nrow(data) / 7, digits = 0)
  max_clusters <- round (nrow(data) / 4, digits = 0)
  cluster_size_offset <- 2
  iterations <- 1
  while(num_clusters < max_clusters) {
    if(iterations > 80) {
      num_clusters <- num_clusters + 1
      iterations <- 1
      cluster_size_offset <- 2
    }
    if(iterations %% 20 == 0) {
      cluster_size_offset <- cluster_size_offset + 1
    }
    clusterresults <- kmeans(mostrecent[,2], num_clusters)
    centers <- sort(clusterresults$centers)
    centers <- sort(clusterresults$centers, decreasing = TRUE)
    clusterresults <- kmeans(mostrecent[,2], num_clusters, centers = centers)
    if(max(clusterresults$size) < (7.5 + cluster_size_offset) & min(clusterresults$size > (6.5 - (cluster_size_offset/1.5)))) {
      clusterresults <<- clusterresults
      return(clusterresults$size)
    }
    iterations <- iterations + 1
  }
  print("Optimal cluster sizes not found.")
  quit()
}

today <- Sys.Date()
plot_predictions_clusters("2021-12-01", today)