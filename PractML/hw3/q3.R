library(pgmm)
library(tree)
data(olive)
olive = olive[,-1]

model <- tree(Area ~., data=olive)
newdata = as.data.frame(t(colMeans(olive)))
predict(model, newdata=newdata)
