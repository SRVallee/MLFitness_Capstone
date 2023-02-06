import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Sample data
X = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0], [4.0, 8.0, 12.0]]) #training data how does this work? why is it 3 nums instead of 4?
#while the test is 4 nums? what is this
y = np.array([0, 0, 1, 1]) # test

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Predict on the test data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
#In this example, the sample data X and y represent the input features and target labels, respectively. The data is split into a training set (80%) and a test set (20%) using the train_test_split function. Then, a support vector machine (SVM) model is trained on the training data using the fit method. The model is used to make predictions on the test data using the predict method, and the accuracy is calculated using the accuracy_score function from the sklearn.metrics module.

#Note: The input features in this example are just for demonstration purposes and do not represent actual features of human bodies. In a real-world scenario, you would use relevant features for the classification task.




