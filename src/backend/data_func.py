from PyQt6.QtWidgets import (
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QListWidget)
from PyQt6.QtGui import QColor
import pandas as pd
import sqlite3


class Funcs:
    """
    Clase que encapsula funciones para la gestión de datos y la interacción con una interfaz gráfica creada con PyQt6.
    """

    def __init__(self, target_combo: QListWidget, features_list: QListWidget, path: QLabel, table: QTableWidget) -> None:
        """
        Inicializa una instancia de la clase Funcs.

        Parámetros:
            target_combo (QListWidget): Widget para seleccionar la columna objetivo.
            features_list (QListWidget): Widget para seleccionar las columnas de características.
            path (QLabel): Etiqueta para mostrar la ruta del archivo.
            table (QTableWidget): Tabla para mostrar los datos cargados.
        """
        self.df = None
        self.input_col = []
        self.target_combo = target_combo
        self.features_list = features_list
        self.file_path_label = path
        self.table_widget = table

    def almacenar(self):
        """
        Almacena las columnas seleccionadas como entrada y objetivo, mostrando mensajes de validación según sea necesario.
        """
        current_item = self.target_combo.currentItem()
        if current_item is None:
            QMessageBox.warning(
                None, "Warning", "Please select at least an input and an output column")
            return

        self.output_col = current_item.text()

        if not self.input_col:
            QMessageBox.warning(
                None, "Warning", "Please select at least an input and an output column")
        else:
            self.output_col = self.target_combo.currentItem().text()
            message = "Your selection has been successfully saved.\n"
            QMessageBox.information(None, "Information", message)

    def load_file(self):
        """
        Abre un cuadro de diálogo para cargar un archivo CSV, XLSX o SQLite, actualizando la interfaz con los datos cargados.
        """
        file_name, _ = QFileDialog.getOpenFileName(None, "Open CSV/XLSX/SQLite", "",
                                                   "CSV Files (*.csv);;Excel Files (*.xlsx);;SQLite Files (*.sqlite);;All Files (*)")
        try:
            if file_name:
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
                self.update_table(self.table_widget, self.df)
                self.mostrar_columnas()
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error reading file: {str(e)}")

    def load_sqlite(self, file_name: str):
        """
        Carga datos desde una base de datos SQLite.

        Parámetros:
            file_name (str): Ruta del archivo SQLite.
        """
        conn = sqlite3.connect(file_name)

        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        if tables.empty:
            QMessageBox.warning(
                None, "Warning", "No tables found in SQLite database.")

    def mostrar_columnas(self):
        """
        Muestra las columnas del DataFrame cargado en los widgets de selección de entrada y objetivo.
        """
        if self.df is not None:
            self.features_list.clear()
            self.features_list.addItems(self.df.columns)
            self.target_combo.clear()
            self.target_combo.addItems(self.df.columns)
        else:
            QMessageBox.warning(None, "Warning", "There is no file uploaded.")

    def update_table(self, table_widget: QTableWidget, df: pd.DataFrame):
        """
        Actualiza el widget de tabla con los datos del DataFrame.

        Parámetros:
            table_widget (QTableWidget): Widget de tabla a actualizar.
            df (pd.DataFrame): DataFrame con los datos a mostrar.
        """
        table_widget.setRowCount(df.shape[0])
        table_widget.setColumnCount(df.shape[1])
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = df.iat[i, j]
                table_item = QTableWidgetItem(str(value))
                if pd.isna(value):
                    table_item.setBackground(QColor("red"))
                table_widget.setItem(i, j, table_item)

    def registrar_input(self):
        """
        Registra las columnas seleccionadas como entradas y actualiza la lista de columnas seleccionadas.
        """
        input_col_text = self.features_list.currentItem().text()
        if input_col_text in self.input_col:
            self.input_col.remove(input_col_text)
        else:
            self.input_col.append(input_col_text)
