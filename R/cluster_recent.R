library(stats)

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