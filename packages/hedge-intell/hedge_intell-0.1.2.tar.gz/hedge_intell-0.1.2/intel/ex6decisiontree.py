import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

# Load data
data = pd.read_csv(r"C:\Users\rajal\Downloads\diabetes.csv")

# Split data into training and test sets
X = data.drop(["Outcome"], axis=1)
y = data["Outcome"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build decision tree
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)

# Predict on test set
y_pred_dt = dt.predict(X_test)
y_pred_dt_binary = [1 if pred >= 0.5 else 0 for pred in y_pred_dt] # Convert to binary predictions

# Evaluate performance
mse_dt = mean_squared_error(y_test, y_pred_dt)
accuracy_dt = accuracy_score(y_test, y_pred_dt_binary)
print(f"Decision Tree Mean Squared Error: {mse_dt:.4f}")
print(f"Decision Tree Accuracy: {accuracy_dt:.4f}")

# Build random forest
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

# Predict on test set
y_pred_rf = rf.predict(X_test)
y_pred_rf_binary = [1 if pred >= 0.5 else 0 for pred in y_pred_rf] # Convert to binary predictions

# Evaluate performance
mse_rf = mean_squared_error(y_test, y_pred_rf)
accuracy_rf = accuracy_score(y_test, y_pred_rf_binary)
print(f"Random Forest Mean Squared Error: {mse_rf:.4f}")
print(f"Random Forest Accuracy: {accuracy_rf:.4f}")
