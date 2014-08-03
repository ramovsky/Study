library(ElemStatLearn)
data(vowel.train)
data(vowel.test) 

vowel.test$y <- as.factor(vowel.test$y)
vowel.test$y <- as.factor(vowel.train$y)

set.seed(33833)
library(caret)

mod_rf <- train(y~., method='rf', data=vowel.train,
                trControl=trainControl(method='cv'), number=3)
mod_gbm <- train(y~., method='gbm', data=vowel.train)

pred_rf <- predict(mod_rf, vowel.test)
pred_gbm <- predict(mod_gbm, vowel.test)

pred_df <- data.frame(pred_rf, pred_gbm, y=vowel.test$y)
mod_comb <- train(y~., method='gam', data=pred_df)
pred_comb <- predict(mod_comb, pred_df)

accur_rf <- 1 - sqrt(sum((pred_rf - vowel.test$y)^2))/length(pred_gbm)
accur_gbm <- 1 - sqrt(sum((pred_gbm - vowel.test$y)^2))/length(pred_gbm)
accur_comb <- 1 - sqrt(sum((pred_comb - vowel.test$y)^2))/length(pred_gbm)

