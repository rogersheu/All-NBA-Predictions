library(directlabels)
library(scales)
library(RColorBrewer)
library(randomcoloR)

plot_Nplayers <- function(data, startIndex, endIndex, endDate) {
  data_subset <- data[startIndex:endIndex,]
  names <- data[startIndex:endIndex,1]

  top_picks <- factor(c(names), levels = c(names)) #automatically alphabetizes so you need to avoid it
  
  melted_players <- melt(data_subset, id='Player')
  
  
  player_names <- melted_players['Player']

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
  

  for(i in 1:nrow(player_names)) {
    player_names[i,1] <- convert_name(player_names[i,1])
  }
  
  melted_players['Player'] <- player_names
  
  melted_players <<- melted_players
  
  lastDate <- melted_players[nrow(melted_players),2]
  range <-  c(as.Date("2021-12-01"), as.Date(endDate) + 3)
  
  lineplot <- ggplot(data=melted_players, aes(x=as.Date(variable), y=value, group=Player)) +
    geom_line(size=1, color = melted_players$color, group=melted_players$Player) + 
    geom_point(size=2, color = melted_players$color, group=melted_players$Player) +
    theme_bw() + 
    theme(panel.grid.minor.x = element_blank()) +
    theme(panel.grid.minor.y = element_blank()) +
    theme(legend.position="none") +
    theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1, size = 12)) +
    xlab("") + 
    ylab("Avg Probability") +
    theme(axis.title.y = element_text(size = 14)) + 
    theme(axis.text.y = element_text(size = 12)) + 
    scale_x_date(date_breaks = "3 days", limits = range) + 
    geom_dl(aes(label = Player), color = melted_players$color, group=melted_players$Player, method = list(dl.trans(x = x + 0.2), "last.bumpup", cex = .9))

  #These global assignments are for sanity checking and could just as easily be removed.
  lineplot <<- lineplot 
  print(lineplot)
  
  ggsave(
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

