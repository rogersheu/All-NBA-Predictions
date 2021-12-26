library(nbastatR)
data <- all_nba_teams()
allNBAplayers <- data[,3:5]
allNBAplayers$numberAllNBATeam <- NULL
write.csv(allNBAplayers, 'listofallNBAteams.csv')


df <- allstar_or_allNBA_stats
df <- subset(df, select = -c(allstarFlag, allNBAFlag))
corrplot(cor(df[, unlist(lapply(df, is.numeric))]), method="number")