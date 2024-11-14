from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
import pandas as pd
from PyQt6.QtGui import QColor
import sqlite3
class Data:
    def __init__(self) -> None:
        self.layout = QVBoxLayout()
        self.inicializarUI()
    def inicializarUI(self):
        self.viewer_title = QLabel("Visualización de los datos")
        self.viewer_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        self.table_widget = QTableWidget()
        self.table_widget.setFixedSize(1180, 500)
        self.load_button = QPushButton("Abrir")
        self.load_button.setFixedSize(60, 30)

        #self.load_button.setStyleSheet("background-color: green; color: black;")
        self.load_button.clicked.connect(self.load_file)

        self.layout.addWidget(self.viewer_title)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.table_widget)


        self.file_path_label = QLabel("Ruta del archivo: Ningún archivo cargado.")
        self.layout.addWidget(self.file_path_label)  # Añadir la etiqueta al layout

        self.features_list = QListWidget()
        self.target_combo = QListWidget()

        self.layout.setContentsMargins(0,20,0,20)


    def get_layout(self):
        return self.layout
    
    def load_file(self):
        print("prueba")
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir CSV/XLSX/SQLite", "",
                                                    "CSV Files (*.csv);;Excel Files (*.xlsx);;SQLite Files (*.sqlite);;All Files (*)")
        try:
            if file_name:
                # Mostrar la ruta del archivo en la etiqueta
                self.file_path_label.setText(f"Ruta del archivo: {file_name}")

                if file_name.endswith('.csv'):
                    self.df = pd.read_csv(file_name)
                elif file_name.endswith('.xlsx'):
                    self.df = pd.read_excel(file_name)
                elif file_name.endswith('.sqlite'):
                    self.load_sqlite(file_name)
                else:
                    QMessageBox.warning(self, "Advertencia", "Formato de archivo no soportado.")
                    return
                self.update_table()  # Actualizamos la tabla al cargar el archivo
                self.mostrar_columnas()
        except Exception as e:
            QMessageBox.warning(self,"Error",f"Error al leer el archivo: {str(e)}")
                # Función para mostrar columnas en la tabla

    def mostrar_columnas(self):
        if self.df is not None:
        # Poblar los selectores con las columnas del DataFrame
            self.features_list.clear()  # Limpiar lista anterior
            self.features_list.addItems(self.df.columns)  # Añadir las columnas al selector de características
            self.target_combo.clear()  # Limpiar la selección anterior del target
            self.target_combo.addItems(self.df.columns)  # Añadir las columnas al combo de target
        else:
            QMessageBox.warning(self, "Advertencia", "No hay un archivo cargado.")
    def update_table(self):
        self.table_widget.setRowCount(self.df.shape[0])
        self.table_widget.setColumnCount(self.df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                value = self.df.iat[i, j]
                table_item = QTableWidgetItem(str(value))
                # Si el valor es NaN, lo detectamos y coloreamos la celda
                if pd.isna(value):
                    table_item.setBackground(QColor("yellow"))  # Resaltar la celda en amarillo
                self.table_widget.setItem(i, j, table_item)
    def load_sqlite(self, file_name):

        conn = sqlite3.connect(file_name)

        # Obtener el nombre de la primera tabla en la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        if tables.empty:
            QMessageBox.warning(self, "Advertencia", "No se encontraron tablas en la base de datos SQLite.")

if __name__=="__main__":
    data=Data()