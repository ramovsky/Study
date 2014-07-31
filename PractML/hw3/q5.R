library(ElemStatLearn)
data(vowel.train)
data(vowel.test) 

vowel.train$y <- factor(vowel.train$y)
vowel.test$y <- factor(vowel.test$y)

library(caret)
set.seed(33833)
modFit5 <- train(y~., data=vowel.train, method="rf")
varImp(modFit5)
