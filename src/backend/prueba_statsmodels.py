import statsmodels.api as sm
from backend.cargar_datos import cargar_datos
import pandas as pd

# Almacenamos los datos del archivo en una variable
data = cargar_datos('housing.csv')

# Eliminamos los valores nulas
data = data.dropna()

# Eliminamos variables categóricas
data = pd.get_dummies(data, drop_first=True)

# Separar características y variable objetivo
X = data.drop("longitude", axis=1)
y = data['latitude']

# Agregar una columna con valores constantes como referencia
X_const = sm.add_constant(X)

# Ajustar el modelo lineal
modelo = sm.OLS(y, X_const).fit()

# Hacer predicciones
predicciones = modelo.predict(X_const)


# Mostrar un resumen con los resultados del modelo
print(modelo.summary())
