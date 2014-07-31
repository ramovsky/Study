library(AppliedPredictiveModeling)
data(segmentationOriginal)
library(caret)

in_train <- split(segmentationOriginal, segmentationOriginal$Case)
train = in_train$Train
test = in_train$Test

set.seed(125)

mod_fit <- train(Class ~ ., method='rpart', data=train)
print(mod_fit$finalModel)
library(rattle)
fancyRpartPlot(mod_fit$finalModel)
