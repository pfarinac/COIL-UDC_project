import sys
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QFileDialog, QPushButton, QMessageBox, QInputDialog, QComboBox, QLabel
from PyQt6.QtGui import QColor

class CsvViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1200, 700)

        self.table_widget = QTableWidget()
        self.load_button = QPushButton("Cargar CSV/XLSX/SQLite")
        self.load_button.clicked.connect(self.load_file)

        self.action_combo_box = QComboBox()
        self.action_combo_box.addItems([
            "Contar Valores Nulos",
            "Eliminar Filas con Nulos",
            "Reemplazar Nulos por Media",
            "Reemplazar Nulos por Mediana",
            "Reemplazar Nulos por Valor"
        ])
        
        self.execute_button = QPushButton("Aplicar preprocesado")
        self.execute_button.clicked.connect(self.execute_action)

        # Añadir etiqueta para mostrar la ruta del archivo
        self.file_path_label = QLabel("Ruta del archivo: Ningún archivo cargado.")
        
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.file_path_label)  # Añadir la etiqueta al layout
        layout.addWidget(self.action_combo_box)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.df = None  # DataFrame para almacenar el archivo cargado

    def load_file(self):
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
        except Exception as e:
            self.mostrar_mensaje_error(f"Error al leer el archivo: {str(e)}")

    def load_sqlite(self, file_name):
        conn = sqlite3.connect(file_name)
        # Obtener el nombre de la primera tabla en la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        
        if tables.empty:
            QMessageBox.warning(self, "Advertencia", "No se encontraron tablas en la base de datos SQLite.")
            return
        
        # Por simplicidad, usar la primera tabla encontrada
        table_name = tables.iloc[0]['name']
        self.df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()

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

    def execute_action(self):
        action = self.action_combo_box.currentText()
        
        if action == "Contar Valores Nulos":
            self.count_nulls()
        elif action == "Eliminar Filas con Nulos":
            self.remove_nulls()
        elif action == "Reemplazar Nulos por Media":
            self.replace_nulls_with_mean()
        elif action == "Reemplazar Nulos por Mediana":
            self.replace_nulls_with_median()
        elif action == "Reemplazar Nulos por Valor":
            self.replace_nulls_with_value()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una acción válida.")

    def count_nulls(self):
        if self.df is not None:
            null_counts = self.df.isnull().sum()
            null_info = "\n".join([f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(self, "Valores Nulos", f"Cantidad de valores nulos por columna:\n{null_info}")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def remove_nulls(self):
        if self.df is not None:
            original_shape = self.df.shape
            self.df.dropna(inplace=True)
            self.update_table()
            QMessageBox.information(self, "Filas Eliminadas", f"Se eliminaron {original_shape[0] - self.df.shape[0]} filas con valores nulos.")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def replace_nulls_with_mean(self):
        if self.df is not None:
            for col in self.df.columns:
                if self.df[col].isnull().any():
                    mean_value = self.df[col].mean()
                    self.df[col].fillna(mean_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Valores Reemplazados", "Los valores nulos han sido reemplazados por la media de cada columna.")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def replace_nulls_with_median(self):
        if self.df is not None:
            for col in self.df.columns:
                if self.df[col].isnull().any():
                    median_value = self.df[col].median()
                    self.df[col].fillna(median_value, inplace=True)
            self.update_table()
            QMessageBox.information(self, "Valores Reemplazados", "Los valores nulos han sido reemplazados por la mediana de cada columna.")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

    def replace_nulls_with_value(self):
        if self.df is not None:
            value, ok = QInputDialog.getText(self, "Reemplazar Nulos por Valor", "Ingrese el valor para reemplazar los nulos:")
            if ok and value:
                for col in self.df.columns:
                    if self.df[col].isnull().any():
                        self.df[col].fillna(value, inplace=True)
                self.update_table()
                QMessageBox.information(self, "Valores Reemplazados", f"Los valores nulos han sido reemplazados por '{value}'.")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un valor válido para reemplazar los nulos.")
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())

