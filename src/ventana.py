from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from PyQt6.QtGui import QFont
import sys
import pandas as pd
import sqlite3
import joblib
from joblib import dump
from PyQt6.QtGui import QColor
from modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QHeaderView

 

class CsvViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado
        self.model = None
        self.input_fields = {}
        self.inicializarUI()

    def inicializarUI(self):
        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1200, 800)

        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        self.viewer_title = QLabel("Data Visualization")
        self.viewer_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 15px;")
        self.viewer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.viewer_title)

        # Botones para abrir archivo y cargar modelo
        layout_open_load = QHBoxLayout()
        self.load_button = QPushButton("Open")
        self.load_button.setFixedSize(100, 42)
        self.load_button.clicked.connect(self.load_file)
        layout_open_load.addWidget(self.load_button)

        self.file_path_label = QLabel("File path: No file uploaded.")
        self.file_path_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-left: 20px;")
        layout_open_load.addWidget(self.file_path_label)
        layout_open_load.addStretch()
        
        self.load_model_button = QPushButton("Load model")
        self.load_model_button.setFixedSize(150, 42)
        self.load_model_button.clicked.connect(self.load_model)
        layout_open_load.addWidget(self.load_model_button)

        main_layout.addLayout(layout_open_load)

        # Tabla de datos
        self.table_widget = QTableWidget()
        self.table_widget.setMinimumHeight(300)
        main_layout.addWidget(self.table_widget)

        # Selección de columnas (features y target)
        layout_column_selection = QHBoxLayout()

        # Features (entrada)
        layout_input = QVBoxLayout()
        self.features_label = QLabel("Select input columns (features):")
        self.features_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        layout_input.addWidget(self.features_label)

        self.features_list = QListWidget()
        self.features_list.setFixedSize(240, 120)
        self.features_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout_input.addWidget(self.features_list)

        self.confirm_button = QPushButton("Confirm selection")
        self.confirm_button.setFixedSize(150, 40)
        layout_input.addWidget(self.confirm_button)

        layout_column_selection.addLayout(layout_input)

        # Target (salida)
        layout_output = QVBoxLayout()
        self.target_label = QLabel("Select output column (target):")
        self.target_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        layout_output.addWidget(self.target_label)

        self.target_combo = QListWidget()
        self.target_combo.setFixedSize(240, 120)
        self.target_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout_output.addWidget(self.target_combo)

        layout_column_selection.addLayout(layout_output)
        layout_column_selection.addStretch()

        main_layout.addLayout(layout_column_selection)

        # Título para preprocesamiento
        preprocessing_title = QLabel("Data Preprocessing")
        preprocessing_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        main_layout.addWidget(preprocessing_title)

        # Opciones de preprocesamiento
        layout_preprocessing = QHBoxLayout()

        self.btn_count_nulls = QPushButton("Count null values")
        self.btn_count_nulls.setEnabled(False)
        layout_preprocessing.addWidget(self.btn_count_nulls)

        self.btn_remove_nulls = QPushButton("Delete rows with nulls")
        self.btn_remove_nulls.setEnabled(False)
        layout_preprocessing.addWidget(self.btn_remove_nulls)

        self.btn_replace_nulls_mean = QPushButton("Replace nulls with mean")
        self.btn_replace_nulls_mean.setEnabled(False)
        layout_preprocessing.addWidget(self.btn_replace_nulls_mean)

        self.btn_replace_nulls_median = QPushButton("Replace nulls with median")
        self.btn_replace_nulls_median.setEnabled(False)
        layout_preprocessing.addWidget(self.btn_replace_nulls_median)

        self.btn_replace_nulls_value = QPushButton("Replace nulls with constant value")
        self.btn_replace_nulls_value.setEnabled(False)
        layout_preprocessing.addWidget(self.btn_replace_nulls_value)

        main_layout.addLayout(layout_preprocessing)

        # Campo para ingresar un valor constante
        self.constant_input = QLineEdit()
        self.constant_input.setPlaceholderText("Constant value")
        self.constant_input.setEnabled(False)
        self.constant_input.setFixedSize(200, 40)
        main_layout.addWidget(self.constant_input)

        # Descripción del modelo
        self.description_label = QLabel("Model Description (Optional):")
        self.description_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        main_layout.addWidget(self.description_label)

        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Add a description for the model...")
        self.description_text.setFixedHeight(100)
        main_layout.addWidget(self.description_text)

        # Gráfica para visualización futura
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(700, 400)
        self.canvas.setVisible(False)
        main_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botones para guardar modelo y hacer predicción
        layout_buttons = QHBoxLayout()

        self.save_button = QPushButton("Save Model")
        self.save_button.setFixedSize(135, 40)
        self.save_button.setEnabled(False)
        layout_buttons.addWidget(self.save_button)

        self.predict_button = QPushButton("Make Prediction")
        self.predict_button.setFixedSize(135, 40)
        self.predict_button.setEnabled(False)
        layout_buttons.addWidget(self.predict_button)

        layout_buttons.addStretch()
        main_layout.addLayout(layout_buttons)

        # Contenedor con scroll
        container = QWidget()
        container.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)

        self.setCentralWidget(scroll_area)
    
    
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
            QMessageBox.warning(self,"Warning","Please select at least an input and an output column")
        else:
            message = "Your selection has been successfully saved.\n"
            QMessageBox.information(self,"Information", message)
            self.habilitar_botones_preprocesado(True)  

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV/XLSX/SQLite", "",
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
                    QMessageBox.warning(self, "Warning", "Unsupported file format.")
                    return
                self.update_table()  # Actualizamos la tabla al cargar el archivo
                self.mostrar_columnas()
        except Exception as e:
            QMessageBox.warning(self,"Error",f"Error reading file: {str(e)}")

 
    def load_sqlite(self, file_name):

        conn = sqlite3.connect(file_name)

        # Obtener el nombre de la primera tabla en la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        if tables.empty:
            QMessageBox.warning(self, "Warning", "No tables found in SQLite database.")

    # Función para mostrar columnas en la tabla
    def mostrar_columnas(self):
        if self.df is not None:
        # Poblar los selectores con las columnas del DataFrame
            self.features_list.clear()  # Limpiar lista anterior
            self.features_list.addItems(self.df.columns)  # Añadir las columnas al selector de características
            self.target_combo.clear()  # Limpiar la selección anterior del target
            self.target_combo.addItems(self.df.columns)  # Añadir las columnas al combo de target
        else:
            QMessageBox.warning(self, "Warning", "There is no file uploaded.")

   
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
                    table_item.setBackground(QColor("red"))  # Resaltar la celda en amarillo
                self.table_widget.setItem(i, j, table_item)

 


    def count_nulls(self):

        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join([f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(self, "Null values", f"Number of null values ​​per column:\n{null_info}")
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


    # Método para crear el modelo y mostrar la gráfica
    def start_model(self):
        self.model_input = self.input_col.copy()
        self.model_output = self.output_col
        if self.df is not None and self.model_input and self.model_output:
            self.model, self.r2, self.mse = model(self.df[self.model_input], self.df[self.model_output])
            if len(self.model_input) == 1:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.scatter(self.df[self.model_input], self.df[self.model_output], label='Data')
                ax.plot(self.df[self.model_input], self.model.predict(self.df[self.model_input]), color='red', label='Adjustment')
                ax.set_xlabel(self.model_input[0])
                ax.set_ylabel(self.model_output)
                ax.set_title('Lineal regression')
                ax.legend()
                self.canvas.setVisible(True)
            else:
                QMessageBox.warning(self, "Error", "You must select a single input column to be able to display the graph")
            self.label_r2_mse.setVisible(True)
            self.label_formula.setText(f"The model formula is:\n{self.formula(self.input_col,self.output_col)}")
            self.label_formula.setVisible(True)
            self.label_r2_mse.setText(f"R2= {self.r2} \nMSE= {self.mse}")
            self.canvas.draw()
            self.save_button.setEnabled(True)  # Habilitar el botón de guardado después de crear el modelo
            self.btn_count_nulls.setEnabled(False)
            self.btn_remove_nulls.setEnabled(False)
            self.btn_replace_nulls_mean.setEnabled(False)
            self.btn_replace_nulls_median.setEnabled(False)
            self.btn_replace_nulls_value.setEnabled(False)
            self.model_button.setEnabled(False)
            self.predict_button.setEnabled(True)
            self.enable_prediction()
    # Método para guardar el modelo y sus metadatos en un archivo .joblib
    def save_model(self):
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save model", "", "Joblib Files (*.joblib)")
        
        if file_path:
            model_data = {
                "model": self.model,
                "description": self.description_text.toPlainText(),
                "input_columns": self.model_input,
                "output_column": self.model_output,
                "r2_score": self.r2,
                "mse": self.mse
            }
            try:
                dump(model_data, file_path)
                QMessageBox.information(self, "Saved Successfully", "The model has been saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save model: {str(e)}")

    def load_model(self):
        # Abrir el diálogo de selección de archivo
        file_name, _ = QFileDialog.getOpenFileName(self, "Load model", "", "Model Files (*.pkl *.joblib)")

       

        if file_name:
            try:
                # Cargar el modelo desde el archivo
                loaded_model_data = joblib.load(file_name)
                # Actualizar la interfaz con la información del modelo cargado
                self.display_loaded_model(loaded_model_data)
                # Mostrar mensaje de confirmación de carga
                QMessageBox.information(self, "Load model", "The model has been loaded successfully.")
                self.enable_prediction()
            except Exception as e:
                # Mostrar mensaje de error si el archivo es inválido
                QMessageBox.warning(self, "Error Loading Model", f"Could not load model: {str(e)}")

    def display_loaded_model(self, model_data,):
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
            self.model_input = model_data["input_columns"]
            self.model_output = model_data["output_column"]
            r2_score = model_data.get("r2_score", "N/A")
            mse = model_data.get("mse", "N/A")
            description = model_data.get("description", "No description available.")

            
    
            # Actualizar etiquetas
            self.label_formula.setText(f"Model formula: {self.formula(self.model_input,self.model_output)}")
            self.label_r2_mse.setText(f"R²: {r2_score}  |  MSE: {mse}")
            self.description_text.setText(description)    

    
    def enable_prediction(self):
        # Habilita la funcionalidad de predicción cuando un modelo está disponible
        if self.model:
            self.predict_button.setEnabled(True)
            self.generate_input_fields()

    def generate_input_fields(self):
        # Genera campos de entrada dinámicos basados en las variables de entrada del modelo
        for field_name in self.model.feature_names_in_:
            input_label = QLabel(f"Enter {field_name}:")
            input_field = QLineEdit()
            self.prediction_layout.addWidget(input_label)
            self.prediction_layout.addWidget(input_field)
            self.input_fields[field_name] = input_field
    def make_prediction(self):
        # Realizar predicción utilizando el modelo cargado o creado
        try:
            input_values = []
            for field_name, input_field in self.input_fields.items():
                value = input_field.text()
                if value == "":
                    raise ValueError(f"Please enter a value for {field_name}")
                input_values.append(float(value))

            # Realizar la predicción
            prediction = self.model.predict([input_values])
            self.result_label.setText(f"Prediction result: {prediction[0]:.4f}")
        except ValueError as ve:
            QMessageBox.warning(self, "Incorrect input", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Prediction error", f"Error during prediction: {e}")

    def formula(self, input_col,output_col):
            formula = f"{output_col} = "
            for i in range(len(input_col)):
                formula += f"{input_col[i]}  *  {self.model.coef_[i]}  +  "
            formula += f" {self.model.intercept_}"
            return formula

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QMainWindow {
        background-color: #000000;  /* Fondo negro */
    }
    QWidget {
        background-color: #000000;  /* Fondo negro para widget principal */
    }
    QLabel {
        color: #FFFFFF;            /* Título en blanco */
        font-size: 20px;
        font-weight: bold;
    }
    QLineEdit, QTextEdit {
        background-color: #1E1E1E; /* Gris oscuro para entrada */
        color: #FFFFFF;            /* Texto blanco */
        border: 1px solid #444444; /* Borde gris oscuro */
        padding: 5px;
        font-size: 14px;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #00C853; /* Verde vibrante al enfocar */
    }
    QTableWidget {
        background-color: #1E1E1E; /* Gris oscuro para fondo de tabla */
        color: #FFFFFF;            /* Texto blanco */
        border: 2px solid #00C853; /* Borde verde vibrante */
        gridline-color: #444444;   /* Líneas de cuadrícula grises */
    }
    QHeaderView::section {
        background-color: #2E2E2E; /* Gris oscuro para encabezados */
        color: #FFFFFF;            /* Texto blanco en encabezados */
        font-weight: bold;
        border: 1px solid #444444; /* Borde gris oscuro */
        padding: 4px;
    }
    QPushButton {
        background-color: #00C853; /* Verde vibrante */
        color: #FFFFFF;            /* Texto blanco */
        border: 1px solid #00E676; /* Borde verde más claro */
        padding: 12px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #00E676; /* Verde más claro al pasar el ratón */
    }
    QPushButton:pressed {
        background-color: #00BFA5; /* Verde intenso al presionar */
    }
    QPushButton:disabled {
        background-color: #555555; /* Gris oscuro para botones desactivados */
        color: #AAAAAA;            /* Texto gris claro para botones desactivados */
        border: 1px solid #444444; /* Borde gris más oscuro */
    }
    QListWidget {
        background-color: #2E2E2E; /* Gris oscuro para fondo */
        color: #FFFFFF;            /* Texto blanco */
        border: 2px solid #00C853; /* Borde verde vibrante */
        padding: 5px;
    }
    QListWidget::item {
        color: #FFFFFF;            /* Texto blanco */
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #00C853; /* Verde para elemento seleccionado */
        color: #000000;            /* Texto negro en selección */
    }
    QScrollBar:vertical {
        background: #1E1E1E;       /* Fondo oscuro */
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: #00C853;       /* Verde para el scroll */
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;          /* Sin flechas */
    }
    """)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())