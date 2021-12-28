library(stats)

cluster_recent <- function(data) {
  temp <- data
  data <- filter(temp, !is.na(temp[,ncol(temp)]))
  mostrecent <- data[c(1, ncol(data))] # Names and prob
  num_clusters <- round (nrow(data) / 7, digits = 0)
  while(TRUE) {
    clusterresults <- kmeans(mostrecent[,2], num_clusters)
    centers <- sort(clusterresults$centers)
    centers <- sort(clusterresults$centers, decreasing = TRUE)
    clusterresults <- kmeans(mostrecent[,2], num_clusters, centers = centers)
    if(max(clusterresults$size) < 10 & min(clusterresults$size > 3)) {
      clusterresults <<- clusterresults
      return(clusterresults$size)
    }
  }
}