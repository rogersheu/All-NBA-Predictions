library(directlabels)
library(scales)
library(RColorBrewer)
library(reshape2)

plot_Nplayers <- function(data, startIndex, endIndex, endDate) {
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
  
  # Sends to global environment for inspection if needed.
  # melted_players <<- melted_players
  
  # Adjusts x-axis to be further out to accommodate directlabels
  lastDate <- melted_players[nrow(melted_players),2]
  range <-  c(as.Date("2021-12-01"), as.Date(endDate) + 3)
  
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
    geom_dl(aes(label = Player), color = melted_players$color, group=melted_players$Player, method = list(dl.trans(x = x + 0.2), "last.bumpup", cex = 1))

  #These global assignments are for sanity checking and could just as easily be removed.
  lineplot <<- lineplot 
  print(lineplot)
  
  ggsave(
    ### Decomment this first line and comment the second line if you're doing the Avg > 0.1 filter instead of the Max > 0.5 filter
    #filename = paste("Over 0.1 - Top ", startIndex, "-", endIndex, " players.png", sep=""),
    filename = paste("Top ", startIndex, "-", endIndex, " players.png", sep=""),
    plot = lineplot,
    device = "png",
    path = "~/GitHub/All-Star-Predictions/R/Graphs/lineplots/",
    width = 12,
    height = 9,
    units = "in",
    dpi = 500,
  )
}

