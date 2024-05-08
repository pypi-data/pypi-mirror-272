from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier 
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression 

# Load sample dataset
iris = load_iris() 
print(iris)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3) 

# Build individual models
svc_model = SVC(kernel='linear', probability=True) 
rf_model = RandomForestClassifier(n_estimators=10) 
lr_model = LogisticRegression()

# Create ensemble model
ensemble = VotingClassifier(estimators=[('svc', svc_model), ('rf', rf_model), ('lr', lr_model)], voting='soft')

# Train ensemble model 
ensemble.fit(X_train, y_train) 

# Make predictions on test set
y_pred = ensemble.predict(X_test) 

# Print ensemble model accuracy
print("Ensemble Accuracy:", ensemble.score(X_test, y_test))
