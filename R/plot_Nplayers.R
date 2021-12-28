library(directlabels)
library(scales)
library(RColorBrewer)
library(randomcoloR)

    theme_bw() + 
    theme(panel.grid.minor.x = element_blank()) +
    theme(panel.grid.minor.y = element_blank()) +
    theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1, size = 12)) +
    xlab("") + 
    ylab("Avg Probability") +
    scale_x_date(date_breaks = "3 days") + 
    scale_color_discrete(limits = top_picks)
  
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

