library(caret)

data = read.csv('~/Projects/Learning/AppPython/Accidents_2019.csv')

# check to see if there are missing data
sum(is.na(data))

# Set the radom seed number
set.seed(100)

TrainingIndex <- createDataPartition(data$Accident_Severity, p=0.8, list = FALSE)
TrainingSet <- data[TrainingIndex,]
TestingSet <- data[-TrainingIndex,]

# Build Training model
Model <- train(Accident_Severity ~ ., data = TrainingSet,
               method = "svmPoly",
               na.action = na.omit,
               preProcess = c("scale", "center"),
               trControl = trainControl(method="none"),
               tuneGrid = data.frame(degree=1, scale=1, C=1))

# build model
Model.cv <- train(Accident_Severity ~ ., data = TrainingSet,
                  method = "svmPoly",
                  na.action = na.omit,
                  preProcess = c("scale", "center"),
                  trControl = trainControl(method="cv", number=10),
                  tuneGrid = data.frame(degree=1, scale=1, C=1))

Model.training <- predict(Model, TrainingSet)
