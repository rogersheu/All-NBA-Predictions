library(dplyr)
library(ggplot2)

# Write a function that passes in the date as an input.

# Load relevant daily data
# stats_20211130_modeled <- read_csv("~/GitHub/All-Star-Predictions/baseData/dailystats/2021-11-30/stats_20211130_modeled.csv")
# df <- select(stats_20211130_modeled, Player, RF, SVM, kNN, MLP)
stats_20211201_modeled <- read_csv("~/GitHub/All-Star-Predictions/baseData/dailystats/2021-12-01/stats_20211201_modeled.csv")
df <- select(stats_20211201_modeled, Player, RF, SVM, kNN, MLP)

df$Avg <- rowMeans(subset(df, select = c(RF, SVM, MLP)), na.rm = TRUE) # Removed kNN because it is consistently lower than the other models.
# Perhaps that's indicating that I need to tune the hyperparameters on the other models?
topCandidates <- filter(df, Avg > 0.25)
attach(topCandidates)
topCandidates <- topCandidates[order(-Avg),]
detach(topCandidates)

ggplot(topCandidates, aes(x=Player, y=RF)) + 
  theme_bw() + 
  theme(axis.text.y = element_text(face = "bold")) +
  ylab("Model Probability") +
  xlab("") + 
  scale_y_continuous(breaks=seq(0,1,0.1)) +
  scale_x_discrete(limits = rev(c(topCandidates$Player))) +
  coord_flip() +
  geom_point(aes(x=Player, y=RF, color = "RF"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
  geom_point(aes(x=Player, y=SVM, color = "SVM"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
  geom_point(aes(x=Player, y=kNN, color = "kNN"), position = position_jitter(w=.1), size = 3, alpha = 0.25) + 
  geom_point(aes(x=Player, y=MLP, color = "MLP"), position = position_jitter(w=.1), size = 3, alpha = 0.25) +
  geom_point(aes(x=Player, y=Avg, color = "Avg"), size = 3, alpha = 1) +
  scale_color_manual(values = c("RF" = "springgreen", "SVM" = "goldenrod", "kNN" = "firebrick1", "MLP" = "royalblue", "Avg" = "gray24"))



#allstar_full <- read_csv("~/GitHub/All-Star-Predictions/baseData/allstar_full.csv")
#allstars_2021 <- allstar_full[allstar_full[,"Season"] == 2021,]

#topCandidates$allstar2021 <- match(topCandidates$Player, allstars_2021$Name, nomatch = 0) / match(topCandidates$Player, allstars_2021$Name, nomatch = 0)