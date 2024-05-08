import pandas as pd
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt

# Load the Iris dataset
iris = load_iris()
X = iris.data

# Convert the dataset to a DataFrame
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Perform K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(iris_df)

# Get the cluster labels
cluster_labels = kmeans.labels_

# Add cluster labels to the DataFrame
iris_df['Cluster'] = cluster_labels

# Print the first few rows of the DataFrame along with cluster labels
print(iris_df.head())

# Visualize the clusters (using only two features for plotting)
plt.figure(figsize=(8, 6))
plt.scatter(iris_df.iloc[:, 0], iris_df.iloc[:, 1], c=cluster_labels, cmap='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x', s=200, 
            label='Centroids')
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.title('K-means Clustering of Iris Dataset')
plt.legend()
plt.show()

# Hierarchical clustering
hierarchical = AgglomerativeClustering(n_clusters=3)
hierarchical.fit(X)
# Create a scatter plot of the data colored by Hierarchical cluster assignment
plt.scatter(X[:, 0], X[:, 1], c=hierarchical.labels_)
plt.title("Hierarchical Clustering")
plt.show()