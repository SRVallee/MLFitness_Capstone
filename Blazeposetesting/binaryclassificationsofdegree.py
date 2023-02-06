import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Create a sample dataset with degrees of bend and corresponding labels
data = {'degree_of_bend': [45, 60, 90, 120, 150],
        'label': [0, 0, 0, 1, 1]}
df = pd.DataFrame(data)

# Split the dataset into training and testing data
X = df[['degree_of_bend']]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train a logistic regression model
logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)
print(y_test)
# Make predictions on the testing data
y_pred = logistic_regression.predict(X_test)
print(X_test, y_pred)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

#In this example, we first create a sample dataset with degrees of bend and 
#corresponding labels, where 0 represents degrees of bend less than or equal 
#to 90, and 1 represents degrees of bend greater than 90. We then use the 
#train_test_split function from sklearn.model_selection to split the dataset 
#into training and testing data.

#Next, we train a logistic regression model using the training data and the 
#LogisticRegression class from sklearn.linear_model. We make predictions on 
#the testing data using the predict method and calculate the accuracy of the 
#model using the accuracy_score function from sklearn.metrics.

#Note that this is just a simple example and the accuracy of the model can be 
#improved by using more complex models or by fine-tuning the hyperparameters.