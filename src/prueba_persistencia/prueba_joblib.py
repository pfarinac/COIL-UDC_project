import joblib
from sklearn.linear_model import LinearRegression
import numpy as np

# Datos de entrenamiento (puedes personalizarlos)
X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y_train = np.array([2, 3, 4, 5])

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Mostrar los detalles del modelo entrenado
print("=== Detalles del modelo entrenado ===")
print("Coeficientes:", model.coef_)
print("Intercepto:", model.intercept_)
print("Predicción antes de guardar:", model.predict([[3, 4]]))

# Guardar el modelo en un archivo utilizando joblib
joblib.dump(model, 'linear_model_joblib.joblib')

# Cargar el modelo desde el archivo .pkl con joblib
loaded_model = joblib.load('linear_model_joblib.joblib')

# Mostrar los detalles del modelo cargado
print("\n=== Detalles del modelo cargado ===")
print("Coeficientes:", loaded_model.coef_)
print("Intercepto:", loaded_model.intercept_)
print("Predicción después de cargar:", loaded_model.predict([[3, 4]]))

# Predicciones adicionales
print("\n=== Predicciones adicionales ===")
predicciones = loaded_model.predict([[5, 6], [7, 8], [9, 10]])
print("Predicciones para [5, 6], [7, 8], [9, 10]:", predicciones)
