from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit)
from PyQt6.QtCore import QStandardPaths
import sys
import pandas as pd
import sqlite3
from PyQt6.QtGui import QColor
from modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CsvViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado
        self.inicializarUI()
    
    def inicializarUI(self):
        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1200, 700)
        #self.setStyleSheet("background-color: lightblue;")

        self.table_widget = QTableWidget()
        self.load_button = QPushButton("Abrir")
        self.load_button.setFixedSize(60, 30)
        #self.load_button.setStyleSheet("background-color: green; color: black;")
        self.load_button.clicked.connect(self.load_file)

        
        # Layout auxiliar 
        layoutaux = QHBoxLayout()

        layoutaux.addWidget(self.load_button)
        
        # Añadir etiqueta para mostrar la ruta del archivo
        self.file_path_label = QLabel("Ruta del archivo: Ningún archivo cargado.") 
        layoutaux.addWidget(self.file_path_label)  # Añadir la etiqueta al layout

        # Creamos el layout principal y le añadimos el auxiliar
        layout = QVBoxLayout()
        layout.addLayout(layoutaux)

        layout.addWidget(self.table_widget)

        # Selector para columnas de entrada (features)
        self.features_label = QLabel("Selecciona las columnas de entrada (features):")
        layout.addWidget(self.features_label)
        self.features_list = QListWidget()
        self.features_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.features_list)
             
        # Selector único para la columna de salida
        self.target_label = QLabel("Selecciona la columna de salida (target):")
        layout.addWidget(self.target_label)
        self.target_combo = QComboBox()
        layout.addWidget(self.target_combo)
        
        # Botón para confimar la selección de las columnas 
        confirm = QPushButton("Confirmar selección")
        self.input_col = [] # Lista con las columnas de entrada
        self.output_col = None # Variable str que contiene la columna de salida
        self.features_list.clicked.connect(self.registrar_input)
        confirm.clicked.connect(self.almacenar)
        layout.addWidget(confirm)
       
        # Layout para botones de preprocesado
        preprocesado_layout = QHBoxLayout()

        # Botón para contar valores nulos
        self.btn_count_nulls = QPushButton("Contar Valores Nulos")
        self.btn_count_nulls.setEnabled(False)
        self.btn_count_nulls.clicked.connect(self.count_nulls)
        preprocesado_layout.addWidget(self.btn_count_nulls)

        # Botón para eliminar filas con nulos
        self.btn_remove_nulls = QPushButton("Eliminar Filas con Nulos")
        self.btn_remove_nulls.setEnabled(False)
        self.btn_remove_nulls.clicked.connect(self.remove_nulls)
        preprocesado_layout.addWidget(self.btn_remove_nulls)

        # Botón para reemplazar nulos por media
        self.btn_replace_nulls_mean = QPushButton("Reemplazar Nulos por Media")
        self.btn_replace_nulls_mean.setEnabled(False)
        self.btn_replace_nulls_mean.clicked.connect(self.replace_nulls_with_mean)
        preprocesado_layout.addWidget(self.btn_replace_nulls_mean)

        # Botón para reemplazar nulos por mediana
        self.btn_replace_nulls_median = QPushButton("Reemplazar Nulos por Mediana")
        self.btn_replace_nulls_median.setEnabled(False)
        self.btn_replace_nulls_median.clicked.connect(self.replace_nulls_with_median)
        preprocesado_layout.addWidget(self.btn_replace_nulls_median)

        # Botón para reemplazar nulos por un valor específico
        self.btn_replace_nulls_value = QPushButton("Reemplazar Nulos por Valor")
        self.btn_replace_nulls_value.setEnabled(False)
        self.btn_replace_nulls_value.clicked.connect(self.replace_nulls_with_value)
        preprocesado_layout.addWidget(self.btn_replace_nulls_value)

        # Añadir layout de botones de preprocesado al layout principal
        layout.addLayout(preprocesado_layout)

        # Layout horizontal para las opciones de manejo de NaN
        options_layout = QHBoxLayout()

        # Campo para que el usuario introduzca un valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Valor constante")
        options_layout.addWidget(self.constant_input)

        #Botón para iniciar el modelo de regresión lineal
        self.model_button =  QPushButton("Iniciar modelo")
        self.model_button.setEnabled(False)
        self.model_button.clicked.connect(self.start_model)
        layout.addWidget(self.model_button)

        # Widget para mostrar la gráfica de matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.resize(500,600)
        layout.addWidget(self.canvas)

        self.label_formula = QLabel("")
        self.label_r2_mse = QLabel("")
        layout.addWidget(self.label_formula)
        layout.addWidget(self.label_r2_mse)

        #Campo de texto para la descripcion del modelo
        self.description_label = QLabel("Descripcion del modelo (opcional): ")
        layout.addWidget(self.description_label)
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Agrega una descripcion para el modelo...")
        layout.addWidget(self.description_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Función para registrar las columnas de entrada 
    def registrar_input(self):
        input_col_text = self.features_list.currentItem().text()
        if input_col_text in self.input_col:
            self.input_col.remove(input_col_text)
        else:
            self.input_col.append(input_col_text)
            self.habilitar_botones_preprocesado(False)
    
    def habilitar_botones_preprocesado(self, habilitar):
        self.btn_count_nulls.setEnabled(habilitar)
        self.btn_remove_nulls.setEnabled(habilitar)
        self.btn_replace_nulls_mean.setEnabled(habilitar)
        self.btn_replace_nulls_median.setEnabled(habilitar)
        self.btn_replace_nulls_value.setEnabled(habilitar)

    # Función para almacenar las selecciones de las columnas e imprimir el mensaje por pantalla
    def almacenar(self):
        self.output_col = self.target_combo.currentText()
        self.model_description = self.description_text.toPlainText()
        if self.output_col == None or self.input_col == []:
            QMessageBox.warning(self,"Advertencia","Por favor seleccione al menos una columna de entrada y una de salida")
        else:
            message = "Tu seleccion se ha guardado correactamente.\n"
            if not self.model_description:
                message += "Nota: No se ha añadido ninguna descripcion para el modelo."
            else:
                message += f"Descripcion del modelo: {self.model_description}"
            QMessageBox.information(self,"Información", message)
            self.habilitar_botones_preprocesado(True)   

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
                self.mostrar_columnas()
        except Exception as e:
            QMessageBox.warning(self,"Error",f"Error al leer el archivo: {str(e)}")

    def load_sqlite(self, file_name):
        conn = sqlite3.connect(file_name)
        # Obtener el nombre de la primera tabla en la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        
        if tables.empty:
            QMessageBox.warning(self, "Advertencia", "No se encontraron tablas en la base de datos SQLite.")
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
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
        
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
        
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join([f"{col}: {count}" for col, count in null_counts.items()])
        
            QMessageBox.information(self, "Valores Nulos", f"Cantidad de valores nulos por columna:\n{null_info}")
            self.model_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo CSV, XLSX o SQLite.")
    
    
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
    
    # Función para crear el modelo y mostrar la gráfica
    def start_model(self):
        if self.df is not None and self.input_col and self.output_col:
            modelo, r2, mse = model(self.df[self.input_col], self.df[self.output_col])
            if len(self.input_col) == 1:
                # Limpia la figura antes de dibujar
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                
                # Generar la gráfica
                ax.scatter(self.df[self.input_col], self.df[self.output_col], label='Datos')
                ax.plot(self.df[self.input_col], modelo.predict(self.df[self.input_col]), color='red', label='Ajuste')
                ax.set_xlabel(self.input_col[0])
                ax.set_ylabel(self.output_col)
                ax.set_title('Regresión Lineal')
                ax.legend()
                formula =f"{self.output_col} = {self.input_col[0]} * {modelo.coef_[0]} + {modelo.intercept_} "
                self.label_r2_mse.setText(f"R2= {r2} \nMSE= {mse}")
                self.label_formula.setText(f"La fórmula del modelo es: {formula}")

                # Actualizar el canvas para mostrar la nueva gráfica
                self.canvas.draw()
            else:
                QMessageBox.warning(self, "Error", " Debes seleecionar una unica columna de entrada para poder mostrar la grafica")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())