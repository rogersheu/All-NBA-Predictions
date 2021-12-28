library(directlabels)
library(scales)
library(RColorBrewer)
library(randomcoloR)

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

