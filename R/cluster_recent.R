library(stats)

cluster_recent <- function(data) {
  temp <- data
  data <- filter(temp, !is.na(temp[,ncol(temp)]))
  mostrecent <- data[c(1, ncol(data))] # Names and prob
  num_clusters <- round (nrow(data) / 7, digits = 0)
  iterations <- 0
  while(TRUE) {
    iterations <- iterations + 1
    if(iterations > 25) {
      num_clusters <- num_clusters + 1
      iterations <- 0
    }
    clusterresults <- kmeans(mostrecent[,2], num_clusters)
    centers <- sort(clusterresults$centers)
    centers <- sort(clusterresults$centers, decreasing = TRUE)
    clusterresults <- kmeans(mostrecent[,2], num_clusters, centers = centers)
    if(max(clusterresults$size) < 13 & min(clusterresults$size > 4)) {
      clusterresults <<- clusterresults
      return(clusterresults$size)
    }
  }
}