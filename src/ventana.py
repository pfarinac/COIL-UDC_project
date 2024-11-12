from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
import sys
import pandas as pd
import sqlite3
import joblib
from joblib import dump
from PyQt6.QtGui import QColor
from modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

 

class CsvViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado
        self.model = None
        self.inputs = []
        self.inicializarUI()

    def inicializarUI(self):

        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1200, 700)

       
       
        layout = QVBoxLayout()

        # Botón para cargar modelo
        self.load_model_button = QPushButton("Cargar Modelo")
        self.load_model_button.clicked.connect(self.load_model)
        layout.addWidget(self.load_model_button)

        # Área de predicción
        self.prediction_area = QWidget()
        self.prediction_layout = QVBoxLayout()
        
        layout.addWidget(self.prediction_area)

        # Botón de predicción
        self.predict_button = QPushButton("Realizar Predicción")
        self.predict_button.setEnabled(False)  # Deshabilitado hasta que un modelo esté disponible
        self.predict_button.clicked.connect(self.make_prediction)
        layout.addWidget(self.predict_button)

        self.output_label = QLabel("Salida del Modelo:")
        self.prediction_layout.addWidget(self.output_label)

        # Mensaje de error
        self.error_message = QLabel("")
        self.prediction_layout.addWidget(self.error_message)

        self.prediction_area.setLayout(self.prediction_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
       
       
        #self.setStyleSheet("background-color: lightblue;")

        self.viewer_title = QLabel("Visualización de los datos")
        self.viewer_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        self.table_widget = QTableWidget()
        self.table_widget.setFixedSize(1180, 500)
        self.load_button = QPushButton("Abrir")
        self.load_button.setFixedSize(60, 30)

        #self.load_button.setStyleSheet("background-color: green; color: black;")
        self.load_button.clicked.connect(self.load_file)

        # Crear un área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Layout auxiliar 
        layoutaux = QHBoxLayout()
        layoutaux.addWidget(self.load_button)
        layoutaux.setContentsMargins(0,20,0,20)
        layout_data= QVBoxLayout()
        layout_data.addWidget(self.table_widget)
        layout_data.setContentsMargins(0,0,0,20)
        # Layout auxiliar horizontal selectores
        layout_select = QHBoxLayout()
        layout_entrad = QVBoxLayout()
        layout_salid = QVBoxLayout()

        layout_select.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_entrad.setContentsMargins(0,20,20,20)
        layout_salid.setContentsMargins(20,20,0,20)
        # Añadir etiqueta para mostrar la ruta del archivo
        self.file_path_label = QLabel("Ruta del archivo: Ningún archivo cargado.")
        layoutaux.addWidget(self.file_path_label)  # Añadir la etiqueta al layout

        # Botón de carga de modelo
        self.load_model_button = QPushButton("Cargar Modelo")
        self.load_model_button.setFixedSize(150, 25)
        self.load_model_button.clicked.connect(self.load_model)  # Conectar el botón a la función de carga
        
        # Añadir el botón al layout
        layoutaux.addWidget(self.load_model_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.inout_title = QLabel("Elija las columnas de entrada y salida")
        self.inout_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Creamos el layout principal y le añadimos los auxiliares
        layout = QVBoxLayout()
        layout.addWidget(self.viewer_title)
        layout.addLayout(layoutaux)
        layout.addLayout(layout_data)
        layout.addWidget(self.inout_title)
        layout_select.addLayout(layout_entrad)
        layout_select.addLayout(layout_salid)
        layout.addLayout(layout_select)
        layout.addWidget(self.load_model_button)
        layout.addWidget(self.prediction_area)
        layout.addWidget(self.predict_button)

        # Selector para columnas de entrada (features)
        self.features_label = QLabel("Selecciona las columnas de entrada (features):")
        layout_entrad.addWidget(self.features_label)
        self.features_list = QListWidget()
        self.features_list.setFixedSize(245, 60)
        self.features_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout_entrad.addWidget(self.features_list)
             
        # Selector único para la columna de salida
        self.target_label = QLabel("Selecciona la columna de salida (target):")
        layout_salid.addWidget(self.target_label)
        self.target_combo = QListWidget()
        self.target_combo.setFixedSize(215, 60)
        self.target_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout_salid.addWidget(self.target_combo)
        
        # Botón para confimar la selección de las columnas 
        self.confirm = QPushButton("Confirmar selección")
        self.confirm.setFixedSize(150, 25)
        self.input_col = [] # Lista con las columnas de entrada
        self.output_col = [] # Variable str que contiene la columna de salida
        self.features_list.clicked.connect(self.registrar_input)
        self.confirm.clicked.connect(self.almacenar)
        layout_select.addWidget(self.confirm)
       
        self.prep_title = QLabel("Preprocesado de datos")
        self.prep_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.prep_title)

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
        preprocesado_layout.setContentsMargins(0,20,0,20)

        # Layout horizontal para las opciones de manejo de NaN
        options_layout = QHBoxLayout()

        # Campo para que el usuario introduzca un valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Valor constante")
        options_layout.addWidget(self.constant_input)

        model_layout = QHBoxLayout()
        self.model_title = QLabel("Visualizar e iniciar modelo")
        self.model_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        #Botón para iniciar el modelo de regresión lineal
        self.model_button =  QPushButton("Iniciar modelo")
        self.model_button.setFixedSize(150, 30)
        self.model_button.setEnabled(False)
        self.model_button.clicked.connect(self.start_model)
        layout.addWidget(self.model_title)
        layout.addWidget(self.model_button)
        model_layout.setContentsMargins(0,20,0,20)
        # Widget para mostrar la gráfica de matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(700, 200)
        self.canvas.setVisible(False)
        model_layout.addWidget(self.canvas)

        formula_layout = QVBoxLayout() 

        self.label_formula = QLabel("")
        self.label_formula.setVisible(False)
        self.label_r2_mse = QLabel("")
        self.label_r2_mse.setVisible(False)
        self.label_formula.setStyleSheet("font-weight: bold;")
        self.label_r2_mse.setStyleSheet("font-weight: bold;")
        formula_layout.addWidget(self.label_formula)
        formula_layout.addWidget(self.label_r2_mse,alignment= Qt.AlignmentFlag.AlignTop)
        model_layout.addLayout(formula_layout)
        layout.addLayout(model_layout)



        #Campo de texto para la descripcion del modelo
        self.description_label = QLabel("Descripcion del modelo (opcional): ")
        layout.addWidget(self.description_label)
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Agrega una descripcion para el modelo...")
        layout.addWidget(self.description_text)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

        # Botón para guardar el modelo
        self.save_button = QPushButton("Guardar Modelo")
        self.save_button.setFixedSize(150, 30)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_model)
        layout.addWidget(self.save_button,alignment=Qt.AlignmentFlag.AlignCenter)    


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

        self.output_col = self.target_combo.currentItem().text()
        self.model_description = self.description_text.toPlainText()
        if self.output_col == [] or self.input_col == []:
            QMessageBox.warning(self,"Advertencia","Por favor seleccione al menos una columna de entrada y una de salida")
        else:
            message = "Tu seleccion se ha guardado correactamente.\n"
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


    # Método para crear el modelo y mostrar la gráfica
    def start_model(self):

        if self.df is not None and self.input_col and self.output_col:
            self.model, self.r2, self.mse = model(self.df[self.input_col], self.df[self.output_col])
            if len(self.input_col) == 1:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.scatter(self.df[self.input_col], self.df[self.output_col], label='Datos')
                ax.plot(self.df[self.input_col], self.model.predict(self.df[self.input_col]), color='red', label='Ajuste')
                ax.set_xlabel(self.input_col[0])
                ax.set_ylabel(self.output_col)
                ax.set_title('Regresión Lineal')
                ax.legend()
                formula = f"{self.output_col} = {self.input_col[0]} * {self.model.coef_[0]} + {self.model.intercept_}"
                self.label_r2_mse.setVisible(True)
                self.label_formula.setText(f"La fórmula del modelo es:\n{formula}")
                self.label_formula.setVisible(True)
                self.label_r2_mse.setText(f"R2= {self.r2} \nMSE= {self.mse}")
                self.canvas.draw()
                self.save_button.setEnabled(True)  # Habilitar el botón de guardado después de crear el modelo
                self.canvas.setVisible(True)
            else:
                QMessageBox.warning(self, "Error", "Debes seleccionar una única columna de entrada para poder mostrar la gráfica")
            self.btn_count_nulls.setEnabled(False)
            self.btn_remove_nulls.setEnabled(False)
            self.btn_replace_nulls_mean.setEnabled(False)
            self.btn_replace_nulls_median.setEnabled(False)
            self.btn_replace_nulls_value.setEnabled(False)
            self.model_button.setEnabled(False)
            self.predict_button.setEnabled(True)

    # Método para guardar el modelo y sus metadatos en un archivo .joblib
    def save_model(self):
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Modelo", "", "Joblib Files (*.joblib)")
        
        if file_path:
            model_data = {
                "model": self.model,
                "description": self.description_text.toPlainText(),
                "input_columns": self.input_col,
                "output_column": self.output_col,
                "r2_score": self.r2,
                "mse": self.mse
            }
            try:
                dump(model_data, file_path)
                QMessageBox.information(self, "Guardado Exitoso", "El modelo se ha guardado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el modelo: {str(e)}")

    def load_model(self):
        # Abrir el diálogo de selección de archivo
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar Modelo", "", "Model Files (*.pkl *.joblib)")

       

        if file_name:
            try:
                # Cargar el modelo desde el archivo
                loaded_model_data = joblib.load(file_name)
                # Actualizar la interfaz con la información del modelo cargado
                self.display_loaded_model(loaded_model_data)
                # Mostrar mensaje de confirmación de carga
                QMessageBox.information(self, "Modelo Cargado", "El modelo ha sido cargado exitosamente.")
            except Exception as e:
                # Mostrar mensaje de error si el archivo es inválido
                QMessageBox.warning(self, "Error al Cargar Modelo", f"No se pudo cargar el modelo: {str(e)}")

    def display_loaded_model(self, model_data):
        # Ocultar secciones de carga de datos y selección de columnas
        self.table_widget.hide()
        self.features_label.hide()
        self.features_list.hide()
        self.target_label.hide()
        self.target_combo.hide()
        self.viewer_title.hide()
        self.inout_title.hide()
        self.prep_title.hide()
        self.model_title.hide()
        # Botones de preprocesado
        self.btn_count_nulls.hide()
        self.btn_remove_nulls.hide()
        self.btn_replace_nulls_mean.hide()
        self.btn_replace_nulls_median.hide()
        self.btn_replace_nulls_value.hide()
        self.confirm.hide()
        self.model_button.hide()
        self.load_button.hide()
        self.file_path_label.hide()
        self.save_button.setEnabled(True)
        # Modelo
        self.canvas.hide()
        self.label_formula.setVisible(True)
        self.label_r2_mse.setVisible(True)
        
        # Mostrar los detalles del modelo cargado
        if "model" in model_data:
            self.model = model_data["model"]
            self.input_col = model_data["input_columns"]
            self.output_col = model_data["output_column"]
            r2_score = model_data.get("r2_score", "N/A")
            mse = model_data.get("mse", "N/A")
            description = model_data.get("description", "No hay descripción disponible.")

            # Generar fórmula
            coefs = self.model.coef_
            intercept = self.model.intercept_
            formula = f"{self.output_col} = " + " + ".join(f"{coef:.4f} * {col}" for coef, col in zip(coefs, self.input_col)) + f" + {intercept:.4f}"
    
            # Actualizar etiquetas
            self.label_formula.setText(f"Fórmula del Modelo: {formula}")
            self.label_r2_mse.setText(f"R²: {r2_score}  |  MSE: {mse}")
            self.description_text.setText(description)    

 
    def load_model_predict(self):
        try:
            model_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Modelo", "", "Model Files (*.pkl *.joblib)")
            if model_path:
                self.model = joblib.load(model_path)
                self.update_input_fields()
                self.predict_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el modelo: {str(e)}")
            self.traceback.print_exc()

    def update_input_fields(self):
        # Limpiar campos de entrada previos
        for widget in self.inputs:
            widget.deleteLater()
        self.inputs = []

        # Suponiendo que las variables de entrada del modelo están en `self.model.feature_names_in_`
        if hasattr(self.model, 'feature_names_in_'):
            for feature in self.model.feature_names_in_:
                label = QLabel(feature)
                line_edit = QLineEdit()
                self.prediction_layout.addWidget(label)
                self.prediction_layout.addWidget(line_edit)
                self.inputs.append((feature, line_edit))

    def make_prediction(self):
        try:
            # Obtener valores de entrada
            input_values = []
            for feature, line_edit in self.inputs:
                text = line_edit.text()
                if not text:
                    raise ValueError(f"Por favor, ingrese un valor para {feature}.")
                input_values.append(float(text))

            # Realizar predicción
            prediction = self.model.predict([input_values])[0]
            self.output_label.setText(f"Salida del Modelo: {prediction:.2f}")
            self.error_message.setText("")  # Limpiar errores
        except ValueError as ve:
            self.error_message.setText(str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error en la predicción: {str(e)}")
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())