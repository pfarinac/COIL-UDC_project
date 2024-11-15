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
from data import Data
from preprocesado import Preprocess

 

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

   

        # Crear un área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Layout auxiliar 

        # Layout auxiliar horizontal selectores

        # Añadir etiqueta para mostrar la ruta del archivo


        # Botón de carga de modelo
        self.load_model_button = QPushButton("Cargar Modelo")
        self.load_model_button.setFixedSize(150, 25)
        self.load_model_button.clicked.connect(self.load_model)  # Conectar el botón a la función de carga
        
        # Añadir el botón al layout
        #layoutaux.addWidget(self.load_model_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.inout_title = QLabel("Elija las columnas de entrada y salida")
        self.inout_title.setStyleSheet("font-size: 20px; font-weight: bold;")


        # Creamos el layout principal y le añadimos los auxiliares
        layout = QVBoxLayout()
        self.data = Data(self.df)
        self.preprocess = Preprocess(self.data.df)

        self.prep_title = QLabel("Preprocesado de datos")
        self.prep_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        
        layout_data = self.data.get_layout()
        layout_preprocess = self.preprocess.get_layout()
        layout.addLayout(layout_data)
        layout.addWidget(self.inout_title)
        layout.addWidget(self.inout_title)
        layout.addWidget(self.prep_title)
        #layout.addLayout(layout_preprocess)
        layout.addWidget(self.load_model_button)
        layout.addWidget(self.prediction_area)
        layout.addWidget(self.predict_button)


       





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
        self.canvas.setFixedSize(700, 400)
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








    # Método para crear el modelo y mostrar la gráfica
    def start_model(self):
        self.model_input = self.input_col.copy()
        self.model_output = self.output_col
        if self.df is not None and self.model_input and self.model_output:
            self.model, self.r2, self.mse = model(self.df[self.model_input], self.df[self.model_output])
            if len(self.model_input) == 1:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.scatter(self.df[self.model_input], self.df[self.model_output], label='Datos')
                ax.plot(self.df[self.model_input], self.model.predict(self.df[self.model_input]), color='red', label='Ajuste')
                ax.set_xlabel(self.model_input[0])
                ax.set_ylabel(self.model_output)
                ax.set_title('Regresión Lineal')
                ax.legend()
                formula = f"{self.model_output} = {self.model_input[0]} * {self.model.coef_[0]} + {self.model.intercept_}"
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
                "input_columns": self.model_input,
                "output_column": self.model_output,
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
            self.model_input = model_data["input_columns"]
            self.model_output = model_data["output_column"]
            r2_score = model_data.get("r2_score", "N/A")
            mse = model_data.get("mse", "N/A")
            description = model_data.get("description", "No hay descripción disponible.")

            # Generar fórmula
            coefs = self.model.coef_
            intercept = self.model.intercept_
            formula = f"{self.model_output} = " + " + ".join(f"{coef:.4f} * {col}" for coef, col in zip(coefs, self.model_input)) + f" + {intercept:.4f}"
    
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