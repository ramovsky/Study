library(AppliedPredictiveModeling)
library(ggplot2)
data(concrete)
library(caret)
set.seed(975)
inTrain = createDataPartition(mixtures$CompressiveStrength, p = 3/4)[[1]]
training = mixtures[ inTrain,]
testing = mixtures[-inTrain,]

plot(training$CompressiveStrength)

plot(training$CompressiveStrength, col=cut2(training$Cement, g=4))
plot(training$CompressiveStrength, col=cut2(training$BlastFurnaceSlag, g=4))
plot(training$CompressiveStrength, col=cut2(training$FlyAsh, g=4))
plot(training$CompressiveStrength, col=cut2(training$Water, g=4))
plot(training$CompressiveStrength, col=cut2(training$Superplasticizer, g=4))
plot(training$CompressiveStrength, col=cut2(training$CoarseAggregate, g=4))
plot(training$CompressiveStrength, col=cut2(training$FineAggregate, g=4))
plot(training$CompressiveStrength, col=cut2(training$Age, g=4))

featurePlot(x=training[, c('Cement','FlyAsh', 'Superplasticizer', 'Age')],
            y=training$CompressiveStrength,
            plot='pairs')
