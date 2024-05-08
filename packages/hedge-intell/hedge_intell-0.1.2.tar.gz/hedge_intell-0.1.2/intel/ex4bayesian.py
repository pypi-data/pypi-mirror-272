import numpy as np
import csv
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

heartDisease = pd.read_csv(r"C:\Users\rajal\OneDrive\Documents\heart disease.csv")
heartDisease = heartDisease.replace('?', np.nan)

print('Few examples from the dataset are given below')
print(heartDisease.head())

Model = BayesianNetwork([('age', 'trestbps'), ('age', 'fbs'), ('gender', 'trestbps'),
                         ('exang', 'trestbps'), ('trestbps', 'heartdisease'), ('fbs', 'heartdisease'),
                         ('heartdisease', 'restecg'), ('heartdisease', 'thalach'), ('heartdisease', 'chol')])

print('\nLearning CPD using Maximum likelihood estimators')
Model.fit(heartDisease, estimator=MaximumLikelihoodEstimator)

print('\nInferencing with Bayesian Network:')

HeartDisease_infer = VariableElimination(Model)
print('\n1. Probability of HeartDisease given Age=30')
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'age': 63})
print(q)

print('\n2. Probability of HeartDisease given cholesterol=100')
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'chol': 204})
print(q)
