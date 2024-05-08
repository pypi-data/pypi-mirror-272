import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics

# Load Data
data_url = r"C:\Users\rajal\OneDrive\Documents\dataset.txt"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)

# Prepare Features and Target
X = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
y = raw_df.values[1::2, 2]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

# Build Linear Regression Model
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)

# Print Coefficients and Variance Score
print('Coefficients: ', reg.coef_)
print('Variance score: {}'.format(reg.score(X_test, y_test)))

# Plot Residual Errors
plt.style.use('fivethirtyeight')
plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color="green", s=10, label='Train data')
plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test, color="blue", s=10, label='Test data')
plt.plot(reg.predict(X_train), np.zeros_like(reg.predict(X_train)), color="red", linewidth=2)
plt.legend(loc='upper right')
plt.title("Residual errors")
plt.show()
