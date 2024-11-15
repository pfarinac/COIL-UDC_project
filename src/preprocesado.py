from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from joblib import dump
from PyQt6.QtGui import QColor
from modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Preprocess:
    def __init__(self,df) -> None:
        self._layout = QVBoxLayout()
        # Layout para botones de preprocesado
        preprocesado_layout = QHBoxLayout()
        self.df = df
        # Botón para contar valores nulos
        self.btn_count_nulls = QPushButton("Contar Valores Nulos")
        self.btn_count_nulls.clicked.connect(self.count_nulls)
        preprocesado_layout.addWidget(self.btn_count_nulls)

        # Botón para eliminar filas con nulos
        self.btn_remove_nulls = QPushButton("Eliminar Filas con Nulos")
        self.btn_remove_nulls.clicked.connect(self.remove_nulls)
        preprocesado_layout.addWidget(self.btn_remove_nulls)

        # Botón para reemplazar nulos por media
        self.btn_replace_nulls_mean = QPushButton("Reemplazar Nulos por Media")
        self.btn_replace_nulls_mean.clicked.connect(self.replace_nulls_with_mean)
        preprocesado_layout.addWidget(self.btn_replace_nulls_mean)

        # Botón para reemplazar nulos por mediana
        self.btn_replace_nulls_median = QPushButton("Reemplazar Nulos por Mediana")
        self.btn_replace_nulls_median.clicked.connect(self.replace_nulls_with_median)
        preprocesado_layout.addWidget(self.btn_replace_nulls_median)

        # Botón para reemplazar nulos por un valor específico
        self.btn_replace_nulls_value = QPushButton("Reemplazar Nulos por Valor")
        self.btn_replace_nulls_value.clicked.connect(self.replace_nulls_with_value)
        preprocesado_layout.addWidget(self.btn_replace_nulls_value)

        # Añadir layout de botones de preprocesado al layout principal
        self._layout.addLayout(preprocesado_layout)
        preprocesado_layout.setContentsMargins(0,20,0,20)

        # Layout horizontal para las opciones de manejo de NaN
        options_layout = QHBoxLayout()

        # Campo para que el usuario introduzca un valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Valor constante")
        options_layout.addWidget(self.constant_input)

        self._layout.setEnabled(False)
    def count_nulls(self):

        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join([f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(self, "Valores Nulos", f"Cantidad de valores nulos por columna:\n{null_info}")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(None, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

   
    def remove_nulls(self):

        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]
            original_shape = self.df.shape
            self.df.dropna(subset=columns_to_process, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Filas Eliminadas", f"Se eliminaron {original_shape[0] - self.df.shape[0]} filas con valores nulos en las columnas seleccionadas.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def replace_nulls_with_mean(self):

        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
       
            for col in columns_to_process:
                if self.df[col].isnull().any():
                    mean_value = self.df[col].mean()
                    self.df[col].fillna(mean_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Valores Reemplazados", "Los valores nulos han sido reemplazados por la media de las columnas seleccionadas.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

 
    def replace_nulls_with_median(self):

        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]
       
            for col in columns_to_process:
                if self.df[col].isnull().any():
                    median_value = self.df[col].median()
                    self.df[col].fillna(median_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Valores Reemplazados", "Los valores nulos han sido reemplazados por la mediana de las columnas seleccionadas.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def replace_nulls_with_value(self):

        if self.df is not None:
            value, ok = QInputDialog.getText(self, "Reemplazar Nulos por Valor", "Ingrese el valor para reemplazar los nulos:")
            if ok and value:
                columns_to_process = self.input_col + [self.output_col]

                for col in columns_to_process:
                    if self.df[col].isnull().any():
                        self.df[col].fillna(value, inplace=True)
                self.update_table()
                QMessageBox.information(self, "Valores Reemplazados", f"Los valores nulos han sido reemplazados por '{value}' en las columnas seleccionadas.")
                self.model_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un valor válido para reemplazar los nulos.")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def get_layout(self):
        return self._layout