def practical6():
    print('''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

"""# Load the dataset from CSV"""

iris_df = pd.read_csv('IRIS.csv')

"""# Display the first few rows of the dataset and its information"""

print(iris_df.head())

print(iris_df.info())

print(iris_df.isnull().sum())

"""# Separate features (X) and target variable (y)"""

X = iris_df.drop('species', axis=1)
y = iris_df['species']

"""# Splitting the dataset into training and testing sets

"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""# Training the Naïve Bayes model"""

model = GaussianNB()
model.fit(X_train, y_train)

"""# Making predictions"""

y_pred = model.predict(X_test)

"""# Displaying predictions for a few samples"""

sample_predictions = pd.DataFrame({'Actual Species': y_test, 'Predicted Species': y_pred})

print("Sample Predictions:")
print(sample_predictions.head())

"""# Computing Confusion Matrix"""

conf_matrix = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(conf_matrix)

"""# Extracting TP, FP, TN, FN from the confusion matrix"""

TP = conf_matrix[1][1]
FP = conf_matrix[0][1]
TN = conf_matrix[0][0]
FN = conf_matrix[1][0]

"""# Showing TP, FP, TN, FN from the confusion matrix"""

print("TP ->",TP)
print("FP ->",FP)
print("TN ->",TN)
print("FN ->",FN)

"""# Computing Accuracy"""

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

"""# Computing Error Rate"""

error_rate = 1 - accuracy

print("Error Rate:", error_rate)

"""# Computing Precision"""

precision = precision_score(y_test, y_pred, average='macro')

print("Precision:", precision)

"""# Computing Recall"""

recall = recall_score(y_test, y_pred, average='macro')

print("Recall:", recall)

''')

practical6()