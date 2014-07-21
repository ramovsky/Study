library(AppliedPredictiveModeling)
library(caret)
data(AlzheimerDisease)

adData = data.frame(predictors)
trainIndex = createDataPartition(diagnosis,p=0.5,list=FALSE)
training = adData[trainIndex,]
testing = adData[-trainIndex,]
