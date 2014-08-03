library(e1071)
set.seed(3523)
library(AppliedPredictiveModeling)
data(concrete)
inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]
training = concrete[ inTrain,]
testing = concrete[-inTrain,]

set.seed(325)
mod <- svm(CompressiveStrength ~ ., data = training)
pred <- predict(mod, testing)
sqrt(sum((pred - testing$CompressiveStrength)^2))
