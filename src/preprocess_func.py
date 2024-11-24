from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from PyQt6.QtGui import QFont
class PFuncs:
    def __init__(self,rem:QPushButton,r_mean:QPushButton,r_median:QPushButton,r_value:QPushButton) -> None:
        self.btn_remove_nulls = rem
        self.btn_replace_nulls_mean= r_mean
        self.btn_replace_nulls_median = r_median
        self.btn_replace_nulls_value = r_value
    def habilitar_botones_preprocesado(self, habilitar):
        self.btn_remove_nulls.setEnabled(habilitar)
        self.btn_replace_nulls_mean.setEnabled(habilitar)
        self.btn_replace_nulls_median.setEnabled(habilitar)
        self.btn_replace_nulls_value.setEnabled(habilitar)

    def count_nulls(self):

        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join([f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(self, "Null values", f"Number of null values ​​per column:\n{null_info}")
            self.habilitar_botones_preprocesado(True)
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

   
    def remove_nulls(self):

        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]
            original_shape = self.df.shape
            self.df.dropna(subset=columns_to_process, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Deleted Rows", f" {original_shape[0] - self.df.shape[0]} rows with null values in the selectd columns were deleted.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def replace_nulls_with_mean(self):

        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
       
            for col in columns_to_process:
                if self.df[col].isnull().any():
                    mean_value = self.df[col].mean()
                    self.df[col].fillna(mean_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Replaced values", "Null values ​​have been replaced by the mean of the selected columns.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

 
    def replace_nulls_with_median(self):

        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]
       
            for col in columns_to_process:
                if self.df[col].isnull().any():
                    median_value = self.df[col].median()
                    self.df[col].fillna(median_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Replaced values", "Null values ​​have been replaced by the median of the selected columns.")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def replace_nulls_with_value(self):

        if self.df is not None:
            value, ok = QInputDialog.getText(self, "Replace nulls with constant value", "Enter the value to replace nulls:")
            if ok and value:
                columns_to_process = self.input_col + [self.output_col]

                for col in columns_to_process:
                    if self.df[col].isnull().any():
                        self.df[col].fillna(value, inplace=True)
                self.update_table()
                QMessageBox.information(self, "Replaced values", f"Null values has been replaced by '{value}' in the selected columns.")
                self.model_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Warning", "Please enter a valid value to replace nulls.")
        else:
            QMessageBox.warning(self, "Warning", "You must first upload a CSV, XLSX or SQLite file.")
