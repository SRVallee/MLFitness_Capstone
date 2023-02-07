import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Collect and preprocess your data
degrees = np.array([85, 90, 88, 82, 87, 91, 89, 83, 86, 95])
labels = np.array([1, 1, 1, 1, 1, 0, 1, 1, 1, 0])

# Step 2: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(degrees, labels, test_size=0.2, random_state=0)

# Step 3: Choose an appropriate machine learning model
model = LogisticRegression()

# Step 4: Train the model

model.fit(X_train.reshape(-1,1), y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test.reshape(-1,1))
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-Score: ", f1)

# Step 6: Make predictions
new_data = np.array([80, 88, 89, 91, 92, 95])
predictions = model.predict(new_data.reshape(-1,1))
print(predictions)
