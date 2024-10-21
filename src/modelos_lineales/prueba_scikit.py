from sklearn.linear_model import LinearRegression
import pandas as pd

#Almacenamos los datos del archivo en una variable
data=pd.read_csv('housing.csv')

#Seleccionamos nuestras columnas de entrada
x=data[["median_income"]]
y=data[["median_house_value"]]


clf=LinearRegression()

#Entrenamos el módelo de regresión lineal
clf.fit(x,y)

#Calculamos el 
clf.coef_
clf.intercept_

#Predecimos un valor que ya está en los datos para comprobar el funcionamiento
clf.predict([[8.3252]])

#Predecimos un valor que no este en los datos
clf.predict([[10]])

