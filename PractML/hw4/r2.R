library(caret)
library(gbm)
set.seed(3433)
library(AppliedPredictiveModeling)
data(AlzheimerDisease)
adData = data.frame(diagnosis,predictors)
inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]
training = adData[ inTrain,]
testing = adData[-inTrain,]

set.seed(62433)

mod_rf <- train(diagnosis~., method='rf', data=training)
mod_gbm <- train(diagnosis~., method='gbm', data=training)
mod_lda <- train(diagnosis~., method='lda', data=training)

pred_rf <- predict(mod_rf, testing)
pred_gbm <- predict(mod_gbm, testing)
pred_lda <- predict(mod_lda, testing)

pred_df <- data.frame(pred_rf, pred_gbm, pred_lda, diagnosis=testing$diagnosis)
mod_comb <- train(diagnosis~., method='rf', data=pred_df)
pred_comb <- predict(mod_comb, pred_df)

confusionMatrix(pred_rf, testing$diagnosis)$overall
confusionMatrix(pred_gbm, testing$diagnosis)$overall
confusionMatrix(pred_lda, testing$diagnosis)$overall
confusionMatrix(pred_comb, testing$diagnosis)$overall
