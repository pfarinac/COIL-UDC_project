from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMessageBox
from PyQt6.QtCore import QStandardPaths
import sys
import pandas as pd
import sqlite3

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
    
    #Añadir título, medidas, posición a la ventana y configurar el botón
    def inicializarUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Ventana")

        #Crear layout vertical
        layout = QVBoxLayout()

        #Crear botón
        self.button = QPushButton("Añadir Archivo")
        self.button.clicked.connect(self.archivos)
        layout.addWidget(self.button)

        #Crear etiqueta para mostrar la ruta del archivo
        self.ruta_label = QLabel("Ruta del archivo: Ninguno")
        layout.addWidget(self.ruta_label)

        #Crear tabla para mostrar los datos
        self.table = QTableWidget()
        self.table.setRowCount(0)  # sin filas
        self.table.setColumnCount(0)  # sin columnas
        layout.addWidget(self.table)

        self.setLayout(layout)

    def mostrar_mensaje_error(self, mensaje):
        """Muestra un cuadro de diálogo de error con el mensaje proporcionado."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)
        msg.exec()

    def archivos(self):

        # Se establece que el explorador de archivos se abrirá en Descargas
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )
        
        # Tipos de archivos aceptados
        file_types = "CSV files (*.csv);;Excel files(*.xlsx);;Excel files(*.xls);;Sqlite files(*.sqlite);;DB files(*.db)"

        # Añadimos todas las configuraciones hechas
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", initial_dir, file_types)

        # Establecemos la condición para cuando se seleccione un archivo
        if file_path:
            
            # Actualizamos la etiqueta con la ruta del archivo
            self.ruta_label.setText(f"Ruta del archivo: {file_path}")

            try:
                # Cargamos los datos según el tipo de archivo
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path)
                elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                    df = pd.read_excel(file_path)
                elif file_path.endswith(".sqlite") or file_path.endswith(".db"):
                    conn = sqlite3.connect(file_path)
                    query = "SELECT name FROM sqlite_master WHERE type='table';"
                    tables = pd.read_sql(query, conn)

                    # Cargamos la primera tabla de la base de datos
                    df = pd.read_sql(f"SELECT * FROM {tables.iloc[0, 0]}", conn)
                    conn.close()
                else:
                    self.mostrar_mensaje_error("Archivo no compatible.")
                    return

                # Mostramos los datos en la tabla
                self.mostrar_datos(df)

            except (pd.errors.EmptyDataError, pd.errors.ParserError):
                self.mostrar_mensaje_error("El archivo CSV está dañado o no es compatible.")
            except FileNotFoundError:
                self.mostrar_mensaje_error("Archivo no encontrado.")
            except sqlite3.DatabaseError:
                self.mostrar_mensaje_error("El archivo SQLite está dañado o no es compatible.")
            except Exception as e:
                self.mostrar_mensaje_error(f"Error al leer el archivo: {str(e)}")

    # Implementamos la función para mostrar los datos
    def mostrar_datos(self, df):
        
        # Establecemos el número de filas y columnas de la tabla
        self.table.setRowCount(len(df.index))  # número de filas en el dataframe
        self.table.setColumnCount(len(df.columns))  # número de columnas en el dataframe

        # Establecemos los nombres de las columnas
        self.table.setHorizontalHeaderLabels(df.columns)

        # Insertamos los datos en la tabla
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
        
        # Ajustamos las columnas
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
