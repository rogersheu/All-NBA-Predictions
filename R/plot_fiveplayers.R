plot_Nplayers <- function(startIndex, endIndex) {
  bestAvg_subset <- bestAvg[startIndex:endIndex,]
  top_picks <- factor(c(bestAvg[startIndex:endIndex,1]), levels = c(bestAvg[startIndex:endIndex,1])) #automatically alphabetizes so you need to avoid it
  
  melted_players <- melt(bestAvg_subset, id='Player')
  lineplot <- ggplot(data=melted_players, aes(x=as.Date(variable), y=value, color=Player, group=Player)) + 
    geom_line(size=1) + 
    geom_point(size=3) +
    theme_bw() + 
    theme(panel.grid.minor.x = element_blank()) +
    theme(panel.grid.minor.y = element_blank()) +
    xlab("Date") + 
    ylim(0,1) + 
    ylab("Avg Probability") +
    scale_x_date(date_breaks = "3 days") + 
    scale_color_discrete(limits = top_picks)
  
  lineplot <<- lineplot
  
  ggsave(
    #filename = paste("AverageFilter - Top ", startIndex-1, "-", endIndex-1, " players.png", sep=""),
    filename = paste("Top ", startIndex-1, "-", endIndex-1, " players.png", sep=""),
    plot = lineplot,
    device = "png", 
    path = "~/GitHub/All-Star-Predictions/R/Graphs/lineplots/",
    width = 8,
    height = 6,
    units = "in",
    dpi = 500,
  )
  print(lineplot)
}
