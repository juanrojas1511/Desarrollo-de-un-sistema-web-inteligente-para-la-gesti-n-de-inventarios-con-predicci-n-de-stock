from sklearn.linear_model import LinearRegression
import numpy as np

meses = np.array([1, 2, 3, 4]).reshape(-1, 1)

ventas = np.array([100, 120, 150, 180])

modelo = LinearRegression()

modelo.fit(meses, ventas)

prediccion = modelo.predict([[5]])

print("Predicción para el mes 5:", prediccion[0])