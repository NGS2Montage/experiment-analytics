df <-read.table("deltaFrequency.csv",header=TRUE, sep=",")
# Interweaving histograms
ggplot(df, aes(x = delta, fill = sessionid)) +
  geom_histogram(breaks=c(seq(0,270,30)), position = "dodge")+
  scale_x_continuous(breaks=c(seq(0,270,30)),seq(0,270,30))+
  ggtitle("") +
  scale_fill_discrete(name = "Sessions")+
  theme(text = element_text(size=20))+
  labs(x = "Time in seconds", y = "Count")
