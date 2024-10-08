import pandas as pd
import sqlite3


def cargar_datos(archivo):
    # Verificar el tipo de archivo por su extensión
    if archivo.endswith('.csv'):
        try:
            df = pd.read_csv(archivo)
            if df.empty:
                raise ValueError("El archivo está vacío")
            print("Archivo CSV cargado.")
        except Exception as e:
            print(f"Carga errónea archivo CSV: {e}")
            return None

    elif archivo.endswith(('.xlsx', '.xls')):
        try:
            df = pd.read_excel(archivo)
            if df.empty:
                raise ValueError("El archivo está vacío")
            print("Archivo Excel cargado.")
        except Exception as e:
            print(f"Carga errónea archivo Excel: {e}")
            return None

    elif archivo.endswith(('.sqlite', '.db')):
        try:
            # Conectarse a la base de datos SQLite
            conn = sqlite3.connect(archivo)
            cursor = conn.cursor()

            # Obtener el nombre de la primera tabla automáticamente
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabla = cursor.fetchone()[0]

            # Cargar los datos de la tabla
            df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
            conn.close()
            if len(tabla) == 0:
                raise ValueError("No se encontraron tablas")
            print("Base de datos SQLite cargada.")
        except Exception as e:
            print(f"Carga errónea base de datos SQLite: {e}")
            return None

    else:
        print("Formato de archivo no soportado.")
        return None

    # Verificar que los datos se hayan cargado correctamente
    if df is not None:
        print("Previsualización de datos cargados:")
        print(df.head())
        return df
    else:
        print("No se pudieron cargar los datos.")
        return None

# Función principal
if __name__ == "__main__":
    archivo = 'housing.xlsx'
    cargar_datos(archivo)
