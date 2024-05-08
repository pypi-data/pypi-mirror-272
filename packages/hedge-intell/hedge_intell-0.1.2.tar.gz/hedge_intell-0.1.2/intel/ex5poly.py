import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

warnings.filterwarnings('ignore')

df = pd.read_csv(r"C:\Users\rajal\Downloads\Position_Salaries.csv")
X = df.iloc[:, 1:2].values
y = df.iloc[:, 2].values

# Simple Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X, y)

# Polynomial Regression - Degree 2
poly_reg2 = PolynomialFeatures(degree=2)
X_poly2 = poly_reg2.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly2, y)

# Polynomial Regression - Degree 3
poly_reg3 = PolynomialFeatures(degree=3)
X_poly3 = poly_reg3.fit_transform(X)
lin_reg_3 = LinearRegression()
lin_reg_3.fit(X_poly3, y)
plt.scatter(X, y, color='red')
plt.plot(X, lin_reg.predict(X), color='green')
plt.title('Simple Linear Regression')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()
# Plotting Polynomial Regression - Degree 2 and Degree 3
plt.style.use('fivethirtyeight')
plt.scatter(X, y, color='red')