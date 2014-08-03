library(lubridate)  # For year() function below
dat = read.csv("~/Study/PractML/hw4/gaData.csv")
training = dat[year(dat$date) < 2012,]
testing = dat[(year(dat$date)) > 2011,]
tstrain = ts(training$visitsTumblr)

library(forecast)
mod <- bats(tstrain)
fcast <- forecast(mod)

plot(fcast); lines(tstrain, col="red")
sum(testing$visitsTumblr<=fcast$upper[,2])/length(testing$visitsTumblr)
