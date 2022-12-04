convert_name <- function(fullName) {
  firstName <- strsplit(fullName, " ", fixed = TRUE)[[1]][1]
  lastName <- strsplit(fullName," ", fixed = TRUE)[[1]][2]
  firstInitial <- paste(substr(firstName, 1, 1), ".", sep="")
  return(paste(firstInitial, lastName, sep=" "))
}
