import pandas as pd
from matplotlib import pyplot as plt
import pylab as pl
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_squared_error,mean_absolute_error
from sklearn.model_selection import train_test_split
from math import sqrt

# Preparando o Dataset
df = pd.read_csv("FuelConsumptionCo2.csv")
motores =  df[['ENGINESIZE']]
co2 = df[['CO2EMISSIONS']]
print(motores.head())

# Separando o Dataset de treino e o Dataset de teste: usando o train_test_split
motores_treino, motores_test, co2_treino, co2_teste = train_test_split(motores, co2, test_size=0.2, random_state=42)
print(type(motores_treino))

# Plotar a correlação entre as features do dataset de treinamento
plt.scatter(motores_treino, co2_treino, color='green')
plt.xlabel("Motor")
plt.ylabel("Emissão de CO2")
plt.show()

# MODELO - REGRESSÃO LINEAR
modelo =  linear_model.LinearRegression()

# .fit = treinar o modelo usando o dataset de TREINO
modelo.fit(motores_treino, co2_treino)
print('(A) Intercepto: ', modelo.intercept_)
print('(B) Inclinação: ', modelo.coef_)

# Plotando a reta de regressão - dataset de TREINO
plt.scatter(motores_treino, co2_treino, color='blue')
plt.plot(motores_treino, modelo.coef_[0][0]*motores_treino + modelo.intercept_[0], '-r')
plt.ylabel("Emissão de C02")
plt.xlabel("Motores")
plt.show()



# EXECUTANDO O MODELO NO DATASET DE TESTE
# 1. Fazendo as predições usando o modelo e base de teste
predCO2 = modelo.predict(motores_test)

# Plotando a reta de regressão - dataset de TESTE
plt.scatter(motores_test, co2_teste, color='blue')
plt.plot(motores_test, modelo.coef_[0][0]*motores_test + modelo.intercept_[0], '-r')
plt.ylabel("Emissão de C02")
plt.xlabel("Motores")
plt.show()



# Avaliando o Modelo
print("Soma dos Erros ao Quadrado (SSE): %.2f " % np.sum((predCO2 - co2_teste)**2))
print("Erro Quadrático Médio (MSE): %.2f" % mean_squared_error(co2_teste, predCO2))
print("Erro Médio Absoluto (MAE): %.2f" % mean_absolute_error(co2_teste, predCO2))
print ("Raiz do Erro Quadrático Médio (RMSE): %.2f " % sqrt(mean_squared_error(co2_teste, predCO2)))
print("R2-score: %.2f" % r2_score(co2_teste, predCO2) )