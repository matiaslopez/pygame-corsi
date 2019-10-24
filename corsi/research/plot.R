setwd("~/repos/matemarote/experiments/corsi")

library(ggplot2)
library(plyr)


table1 = read.csv("theory.csv",sep = ";")

df= data.frame(table1)


df2 <- df[df$NumberMoves<5  & df$NumberMoves>1 ,]

df2 <- df[df$NumberMoves>1 ,]
#df2 <- df[,]

# df2$Leftness <- factor(df2$Leftness)
# df2$Length <- factor(df2$Length)

data2 <- aggregate(df2$Length,by=list(Length=df2$Length,Leftness=df2$Leftness, NumberMoves=df2$NumberMoves),length)
names(data2)[4] <- "count"


p <- ggplot(data2, aes(x=Length,y=Leftness)) + geom_point(aes(size=count)) + 
  geom_smooth(method = "lm", se = TRUE, color = "red", size=2) +
  ggtitle("Realtionship between Length and Leftness") +
  facet_wrap(~ NumberMoves, ncol=4) #, scales="free_x" )

print(p)
ggsave('plots/realtion-length_leftness-weighted.png', width=15, height=10) 


p <- ggplot(df2, aes(x=Length, y=Leftness)) +
  geom_point(size = 1.5, alpha = 0.5) + 
  # geom_point(aes(x=Length, y=Leftness, size=..count..)) + 
  geom_smooth(method = "lm", se = TRUE, color = "red", size=2) +
  ggtitle("Realtionship between Length and Leftness") +
  facet_wrap(~ NumberMoves, ncol=4) #, scales="free_x" )

print(p)
ggsave('plots/realtion-length_leftness.png', width=15, height=10) 

cdata <- ddply(df2, c("NumberMoves"), summarise,
               N    = sum(!is.na(NumberMoves)),
               mean_length = format(round(mean(Length, na.rm=TRUE), 2), nsmall = 2),
               se_length = format(round(sd(Length, na.rm=TRUE) / sqrt(N), 2), nsmall = 2),
               min_length = format(round(min(Length, na.rm=TRUE), 2), nsmall = 2),
               max_length = format(round(max(Length, na.rm=TRUE), 2), nsmall = 2),
               mean_leftness = format(round(mean(Leftness, na.rm=TRUE), 2), nsmall = 2),
               mean_frontness = format(round(mean(Frontness, na.rm=TRUE), 2), nsmall = 2)               
               )


