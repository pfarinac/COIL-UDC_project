from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QStandardPaths
import sys
import pandas as pd
import sqlite3

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None  # Inicializamos el DataFrame vacío
        self.inicializarUI()

    # Inicializamos la interfaz
    def inicializarUI(self):
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("Gestión de Datos Inexistentes")

        # Layout vertical principal
        layout = QVBoxLayout()

        # Botón para añadir archivo
        self.button = QPushButton("Añadir Archivo")
        self.button.clicked.connect(self.archivos)
        layout.addWidget(self.button)

        # Etiqueta para mostrar la ruta del archivo
        self.ruta_label = QLabel("Ruta del archivo: Ninguno")
        layout.addWidget(self.ruta_label)

        # Tabla para mostrar los datos
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Botón para detectar valores inexistentes (NaN)
        self.nan_button = QPushButton("Detectar Valores Inexistentes")
        self.nan_button.clicked.connect(self.detectar_nan)
        layout.addWidget(self.nan_button)

        # Layout horizontal para las opciones de manejo de NaN
        options_layout = QHBoxLayout()

        # ComboBox para elegir cómo manejar los NaN
        self.nan_options = QComboBox()
        self.nan_options.addItems(["Eliminar Filas", "Rellenar con Media", "Rellenar con Mediana", "Rellenar con Valor"])
        options_layout.addWidget(self.nan_options)

        # Campo para que el usuario introduzca un valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Valor constante")
        options_layout.addWidget(self.constant_input)

        # Botón para aplicar el preprocesado
        self.apply_button = QPushButton("Aplicar Preprocesado")
        self.apply_button.clicked.connect(self.aplicar_preprocesado)
        layout.addLayout(options_layout)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    # Función para mostrar mensajes de error
    def mostrar_mensaje_error(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)
        msg.exec()

    # Función para mostrar mensajes informativos
    def mostrar_mensaje_info(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Información")
        msg.setText(mensaje)
        msg.exec()

    # Función para seleccionar y cargar un archivo
    def archivos(self):
        initial_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        file_types = "CSV files (*.csv);;Excel files(*.xlsx);;Excel files(*.xls);;Sqlite files(*.sqlite);;DB files(*.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", initial_dir, file_types)

        if file_path:
            self.ruta_label.setText(f"Ruta del archivo: {file_path}")
            try:
                if file_path.endswith(".csv"):
                    self.df = pd.read_csv(file_path)
                elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                    self.df = pd.read_excel(file_path)
                elif file_path.endswith(".sqlite") or file_path.endswith(".db"):
                    conn = sqlite3.connect(file_path)
                    query = "SELECT name FROM sqlite_master WHERE type='table';"
                    tables = pd.read_sql(query, conn)
                    self.df = pd.read_sql(f"SELECT * FROM {tables.iloc[0, 0]}", conn)
                    conn.close()
                else:
                    self.mostrar_mensaje_error("Archivo no compatible.")
                    return

                self.mostrar_datos(self.df)

            except Exception as e:
                self.mostrar_mensaje_error(f"Error al leer el archivo: {str(e)}")

    # Función para mostrar datos en la tabla
    def mostrar_datos(self, df):
        self.table.setRowCount(len(df.index))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    # Detectar valores NaN en el DataFrame
    def detectar_nan(self):
        if self.df is None:
            self.mostrar_mensaje_error("No se ha cargado ningún archivo.")
            return
        
        nan_summary = self.df.isna().sum()
        nan_columns = nan_summary[nan_summary > 0]

        if nan_columns.empty:
            self.mostrar_mensaje_info("No hay valores inexistentes en el archivo.")
        else:
            mensaje = "Valores inexistentes detectados en:\n"
            for col, count in nan_columns.items():
                mensaje += f"- {col}: {count} valores\n"
            self.mostrar_mensaje_info(mensaje)

    # Aplicar el preprocesado según la opción seleccionada
    def aplicar_preprocesado(self):
        if self.df is None:
            self.mostrar_mensaje_error("No se ha cargado ningún archivo.")
            return

        opcion = self.nan_options.currentText()

        try:
            if opcion == "Eliminar Filas":
                self.df.dropna(inplace=True)
            elif opcion == "Rellenar con Media":
                self.df.fillna(self.df.mean(numeric_only=True), inplace=True)
            elif opcion == "Rellenar con Mediana":
                self.df.fillna(self.df.median(numeric_only=True), inplace=True)
            elif opcion == "Rellenar con Valor":
                valor = self.constant_input.text()
                if valor == "":
                    self.mostrar_mensaje_error("Debe ingresar un valor constante.")
                    return
                self.df.fillna(valor, inplace=True)

            # Actualizamos la tabla con los datos preprocesados
            self.mostrar_datos(self.df)
            self.mostrar_mensaje_info("Preprocesado aplicado correctamente.")

        except Exception as e:
            self.mostrar_mensaje_error(f"Error durante el preprocesado: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
