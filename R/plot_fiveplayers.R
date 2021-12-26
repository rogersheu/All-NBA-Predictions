  ggsave(
    filename = paste("Model Output ", year, month, day, ".png", sep=""),
    plot = lineplot,
    device = "png", 
    path = "~/GitHub/All-Star-Predictions/R/Graphs/",
    width = 12,
    height = 9.75,
    units = "in",
    dpi = 500,
