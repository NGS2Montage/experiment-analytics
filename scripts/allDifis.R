#no normalized Distance
data <-read.table("playerContributions.csv",header=TRUE, sep=",")
data[data == 9999] <- NA

data$session <- as.numeric(data$sessionid)

data$na_count <- apply(data, 1, function(x) sum(is.na(x)))

data = data[data$na_count < 8,]
d1 <- aggregate(data$d1Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d1["difi"] <- 1

d2 <- aggregate(data$d2Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d2["difi"] <- 2

d3 <- aggregate(data$d3Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d3["difi"] <- 3

myData <- rbind(d1,d2,d3)

myData <- do.call(data.frame, myData)

myData$se <- myData$x.sd / sqrt(myData$x.n)

colnames(myData) <- c("Anagrams", "mean", "sd", "n", "difi", "se")

myData$names <- c(paste(myData$Anagrams, "Anagrams /",
                        myData$difi, " difi"))

limits <- aes(ymax = myData$mean + myData$se,
              ymin = myData$mean - myData$se)

p <- ggplot(data = myData, aes(x = factor(difi), y = mean,
                               fill = factor(Anagrams)))

p + geom_bar(stat = "identity",
             position = position_dodge(0.9)) +
  geom_errorbar(limits, position = position_dodge(0.9),
                width = 0.25) +
  labs(x = "Difi", y = "Difi score per player") +
  ggtitle("") +
  theme(text = element_text(size=20))+
  scale_fill_discrete(name = "Game",labels=c("P2","P1+P2"))

#---------------------------#
#normalized Distance

par(mfrow=c(1,1))
data <-read.table("playerContributions.csv",header=TRUE, sep=",")
data[data == 9999] <- NA

data$d1Distance=rescale(data$d1Distance, to=c(0,225))
data$d1Overlap=rescale(data$d1Overlap, to=c(0,225))
data$d2Distance=rescale(data$d2Distance, to=c(0,225))
data$d2Overlap=rescale(data$d2Overlap, to=c(0,225))
data$d3Distance=rescale(data$d3Distance, to=c(0,225))
data$d3Overlap=rescale(data$d3Overlap, to=c(0,225))

data$session <- as.numeric(data$sessionid)

data$na_count <- apply(data, 1, function(x) sum(is.na(x)))

data = data[data$na_count < 8,]
d1 <- aggregate(data$d1Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d1["difi"] <- 1

d2 <- aggregate(data$d2Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d2["difi"] <- 2

d3 <- aggregate(data$d3Distance,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d3["difi"] <- 3

myData <- rbind(d1,d2,d3)

myData <- do.call(data.frame, myData)

myData$se <- myData$x.sd / sqrt(myData$x.n)

colnames(myData) <- c("Anagrams", "mean", "sd", "n", "difi", "se")

myData$names <- c(paste(myData$Anagrams, "Anagrams /",
                        myData$difi, " difi"))

limits <- aes(ymax = myData$mean + myData$se,
              ymin = myData$mean - myData$se)

p <- ggplot(data = myData, aes(x = factor(difi), y = mean,
                               fill = factor(Anagrams)))

p + geom_bar(stat = "identity",
             position = position_dodge(0.9)) +
  geom_errorbar(limits, position = position_dodge(0.9),
                width = 0.25) +
  labs(x = "Difi", y = "Difi score per player") +
  ggtitle("") +
  theme(text = element_text(size=20))+
  scale_fill_discrete(name = "Game",labels=c("P2","P1+P2"))

#---------------------------#

  #no normalized Overlap
  data <-read.table("playerContributions.csv",header=TRUE, sep=",")
data[data == 9999] <- NA

data$session <- as.numeric(data$sessionid)

data$na_count <- apply(data, 1, function(x) sum(is.na(x)))

data = data[data$na_count < 8,]
d1 <- aggregate(data$d1Overlap,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d1["difi"] <- 1

d2 <- aggregate(data$d2Overlap,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d2["difi"] <- 2

d3 <- aggregate(data$d3Overlap,
                by = list(Anagrams = data$anagrams),
                FUN = function(x) c(mean = mean(x,na.rm=TRUE), sd = sd(x,na.rm=TRUE),
                                    n = length(x)))
d3["difi"] <- 3

myData <- rbind(d1,d2,d3)

myData <- do.call(data.frame, myData)

myData$se <- myData$x.sd / sqrt(myData$x.n)

colnames(myData) <- c("Anagrams", "mean", "sd", "n", "difi", "se")

myData$names <- c(paste(myData$Anagrams, "Anagrams /",
                        myData$difi, " difi"))

limits <- aes(ymax = myData$mean + myData$se,
              ymin = myData$mean - myData$se)

p <- ggplot(data = myData, aes(x = factor(difi), y = mean,
                               fill = factor(Anagrams)))

p + geom_bar(stat = "identity",
             position = position_dodge(0.9)) +
  geom_errorbar(limits, position = position_dodge(0.9),
                width = 0.25) +
  labs(x = "Difi", y = "Difi score per player") +
  ggtitle("") +
  theme(text = element_text(size=20))+
  scale_fill_discrete(name = "Game",labels=c("P2","P1+P2"))

