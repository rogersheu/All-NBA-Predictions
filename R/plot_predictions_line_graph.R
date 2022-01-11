plot_predictions_clusters <- function(startDate, endDate) {

  data <- processing_predictions(startDate, endDate)
  
  cluster_sizes <- cluster_recent(data)
  startIndex <- 1
  for(i in 1:length(cluster_sizes)) {
    endIndex <- startIndex + (cluster_sizes[i] - 1)
    plot_Nplayers(data, startIndex, endIndex, endDate, 1)
    startIndex <- endIndex + 1
  }
  
  # for(i in 1:nrow(data)) {
  #   plot_Nplayers(data, i, i, endDate)
  # }  

}


plot_predictions_fixedsubset <- function(startDate, endDate, indices) { 
  startIndex <- indices[0]
  endIndex <- indices[1]
  data <- processing_predictions(startDate, endDate)
  plot_Nplayers(data, startIndex, endIndex, endDate, 0)
}


plot_predictions_all <- function(startDate, endDate) { 
  data <- processing_predictions(startDate, endDate)
  plot_Nplayers(data, 1, nrow(data), endDate, 0)
}