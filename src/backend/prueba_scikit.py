from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
from backend.cargar_datos import cargar_datos

# Almacenamos los datos del archivo en una variable
data = cargar_datos('housing.xlsx')

# Eliminamos valores nulos
data = data.dropna()

# Eliminamos variables categóricas
data = pd.get_dummies(data, drop_first=True)

# Seleccionamos nuestras columnas de entrada
y = data[["latitude"]]
X = data.drop("longitude", axis=1)

# Separamos los valores en aquellos para entrenar el modelo y en los que usaremos para probarlo
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Creamos el modelo de regresión lineal
clf = LinearRegression()

# Entrenamos el módelo de regresión lineal
clf.fit(X_train, y_train)

# Hacemos predicciones
predict = clf.predict(X_test)

# Calculamos el mse
mse = mean_squared_error(y_test, predict)

# Calculamos R²
r2 = r2_score(y_test, predict)

print(f'Error cuadrático medio: {mse}')
print(f'R²: {r2}')
