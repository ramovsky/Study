set.seed(3523)
library(AppliedPredictiveModeling)
data(concrete)
inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]
training = concrete[ inTrain,]
testing = concrete[-inTrain,]

set.seed(233)
library(elasticnet)
library(caret)

model <- train(CompressiveStrength~., method='lasso', data=training)
plot.enet(model$finalModel, xvar = "penalty", use.color = TRUE)
