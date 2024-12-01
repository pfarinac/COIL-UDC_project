from PyQt6.QtWidgets import (
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QListWidget)
from PyQt6.QtGui import QColor
import pandas as pd
import sqlite3

# Función para almacenar las selecciones de las columnas e imprimir el mensaje por pantalla


class Funcs:
    def __init__(self, target_combo: QListWidget, features_list: QListWidget, path: QLabel, table) -> None:
        self.df = None
        self.input_col = []
        self.target_combo = target_combo
        self.features_list = features_list
        self.file_path_label = path
        self.table_widget = table

    def almacenar(self):
        self.output_col = self.target_combo.currentItem().text()
        # model_description = description_text.toPlainText()
        if self.output_col == [] or self.input_col == []:
            QMessageBox.warning(
                None, "Warning", "Please select at least an input and an output column")
        else:
            message = "Your selection has been successfully saved.\n"
            QMessageBox.information(None, "Information", message)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Open CSV/XLSX/SQLite", "",
                                                   "CSV Files (*.csv);;Excel Files (*.xlsx);;SQLite Files (*.sqlite);;All Files (*)")
        try:
            if file_name:
                # Mostrar la ruta del archivo en la etiqueta
                self.file_path_label.setText(f"File path: {file_name}")

                if file_name.endswith('.csv'):
                    self.df = pd.read_csv(file_name)
                elif file_name.endswith('.xlsx'):
                    self.df = pd.read_excel(file_name)
                elif file_name.endswith('.sqlite'):
                    self.load_sqlite(file_name)
                else:
                    QMessageBox.warning(
                        None, "Warning", "Unsupported file format.")
                    return
                # Actualizamos la tabla al cargar el archivo
                self.update_table(self.table_widget, self.df)
                self.mostrar_columnas()
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error reading file: {str(e)}")

    def load_sqlite(self, file_name):

        conn = sqlite3.connect(file_name)

        # Obtener el nombre de la primera tabla en la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        if tables.empty:
            QMessageBox.warning(
                None, "Warning", "No tables found in SQLite database.")

        # Función para mostrar columnas en la tabla
    def mostrar_columnas(self):
        if self.df is not None:
            # Poblar los selectores con las columnas del DataFrame
            self.features_list.clear()  # Limpiar lista anterior
            # Añadir las columnas al selector de características
            self.features_list.addItems(self.df.columns)
            self.target_combo.clear()  # Limpiar la selección anterior del target
            # Añadir las columnas al combo de target
            self.target_combo.addItems(self.df.columns)
        else:
            QMessageBox.warning(None, "Warning", "There is no file uploaded.")

    def update_table(self, table_widget: QTableWidget, df):
        print("PRUEBA")
        table_widget.setRowCount(df.shape[0])
        table_widget.setColumnCount(df.shape[1])
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = df.iat[i, j]
                table_item = QTableWidgetItem(str(value))
                # Si el valor es NaN, lo detectamos y coloreamos la celda
                if pd.isna(value):
                    # Resaltar la celda en amarillo
                    table_item.setBackground(QColor("red"))
                table_widget.setItem(i, j, table_item)

        # Función para registrar las columnas de entrada

    def registrar_input(self):

        input_col_text = self.features_list.currentItem().text()
        if input_col_text in self.input_col:
            self.input_col.remove(input_col_text)
        else:
            self.input_col.append(input_col_text)
