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
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from data_func import *
from data_UI import *

 

class CsvViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado
        self.model = None
        self.input_fields = {}
        self.input_labels = {}
        self.inicializarUI()

    def inicializarUI(self):

        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1920, 1080)
     
        self.d_u = UI()

        layout_count_nulls = QGridLayout()

        # Layout secundario preprocesado
        layout_preprocesado = QVBoxLayout()
        layout_preprocesado.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_preprocesado.setContentsMargins(5, 20, 0, 0)

        # Añadir etiqueta con el titulo
        self.prep_title = QLabel("Data preprocessing")
        self.prep_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout_preprocesado.addWidget(self.prep_title)


        #layout_count_nulls.addWidget(self.btn_count_nulls)
        layout_count_nulls.setContentsMargins(0,7,0,0)
        layout_preprocesado.addLayout(layout_count_nulls)
        
        # Layout resto de botones para nulos
        layout_nulls_buttons = QGridLayout()
        # Eliminar filas con nulos
        self.btn_remove_nulls = QPushButton("Delete rows with nulls")
        self.btn_remove_nulls.setFixedSize(320, 40)
        self.btn_remove_nulls.setEnabled(False)
        self.btn_remove_nulls.clicked.connect(self.remove_nulls)
        layout_nulls_buttons.addWidget(self.btn_remove_nulls, 0, 0)
        # Reemplazar nulos por media
        self.btn_replace_nulls_mean = QPushButton("Replace nulls with mean")
        self.btn_replace_nulls_mean.setFixedSize(320, 40)
        self.btn_replace_nulls_mean.setEnabled(False)
        self.btn_replace_nulls_mean.clicked.connect(self.replace_nulls_with_mean)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_mean, 0, 1)
        # Reemplazar nulos por mediana
        self.btn_replace_nulls_median = QPushButton("Replace nulls with median")
        self.btn_replace_nulls_median.setFixedSize(320, 40)
        self.btn_replace_nulls_median.setEnabled(False)
        self.btn_replace_nulls_median.clicked.connect(self.replace_nulls_with_median)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_median, 1,0)
        # Reemplazar nulos por un valor específico
        self.btn_replace_nulls_value = QPushButton("Replace nulls with constant value")
        self.btn_replace_nulls_value.setFixedSize(320, 40)
        self.btn_replace_nulls_value.setEnabled(False)
        self.btn_replace_nulls_value.clicked.connect(self.replace_nulls_with_value)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_value, 1,1)
        
        # Añadir layouts individuales botones count null values y resto de botones
        layout_preprocesado.addLayout(layout_nulls_buttons)
        layout_preprocesado.setContentsMargins(0,20,0,0)       
        
        # Layout principal entrada y salida y preprocesado
        layout_entrada_salida_preprocesado = QHBoxLayout()
        layout_entrada_salida_preprocesado.addLayout(self.d_u.layout_entrada_salida)
        layout_entrada_salida_preprocesado.addLayout(layout_preprocesado)      
        layout_entrada_salida_preprocesado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Layout para gráfica y fórmula
        layout_graph_formula = QHBoxLayout()
        
        self.graph_widget = QWidget()  # Usamos QWidget en lugar de QGroupBox
        self.graph_widget.setStyleSheet("""
            QWidget {
                font-size: 16px;
                font-weight: bold;
                color: white; /* Texto en blanco */
                background-color: #1E1E1E; /* Fondo gris oscuro */
                border: 2px solid #00C853; /* Borde verde vibrante */
                border-radius: 5px; /* Esquinas redondeadas */
                padding: 10px; /* Espaciado interno */
            }
        """)
        
        # Layout interno para la gráfica
        self.graph_layout = QVBoxLayout()
        self.graph_widget.setLayout(self.graph_layout)
        
        # Título y canvas para la gráfica
        self.graph_title = QLabel("Graph")
        self.graph_title.setStyleSheet("font-weight: bold; font-size: 16px; color: white; background: transparent; border: none;")
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(700, 400)
        self.canvas.setVisible(False)
        
        # Agregar widgets al layout de la gráfica
        self.graph_layout.addWidget(self.graph_title)
        self.graph_layout.addWidget(self.canvas)
        
        # Layout para la fórmula
        self.formula_layout = QVBoxLayout()
        
        # Título y etiqueta para la fórmula
        self.formula_title = QLabel("Formula")
        self.formula_title.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        self.label_formula = QLabel("")
        self.label_formula.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        self.label_formula.setVisible(False)
        self.label_r2_mse = QLabel("")
        self.label_r2_mse.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        self.label_r2_mse.setVisible(False)

        
        # Agregar widgets al layout de la fórmula
        self.formula_layout.addWidget(self.formula_title)
        self.formula_layout.addWidget(self.label_formula)
        self.formula_layout.addWidget(self.label_r2_mse)
        
        # Crear un widget contenedor para la fórmula (opcional)
        self.formula_widget = QWidget()
        self.formula_widget.setLayout(self.formula_layout)
        
        # Estilos solo para el contenedor del widget
        self.formula_widget.setStyleSheet("""QWidget {
            background-color: #1E1E1E;  /* Gris oscuro para fondo */
            border: 2px solid #00C853;  /* Borde verde vibrante */
            border-radius: 5px;         /* Esquinas redondeadas */
            padding: 10px;              /* Espaciado interno */
            }
            QLabel {border: 0px}
        """)

        # Agregar el widget de fórmula al layout principal
        layout_graph_formula.addWidget(self.graph_widget)
        layout_graph_formula.addWidget(self.formula_widget)
        
        
        # Layout decripcion del modelo
        layout_descripcion_modelo = QVBoxLayout()
        layout_descripcion_modelo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Añadir etiqueta con el titulo
        self.description_label = QLabel("Model description (optional): ")
        self.description_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout_descripcion_modelo.addWidget(self.description_label)
        # Añadir etiqueta para escribir descripcion
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Add a description for the model...")
        layout_descripcion_modelo.addWidget(self.description_text)
        
        # Layout visualizar e iniciar modelo
        layout_visualizar_iniciar_modelo = QVBoxLayout()
        #layout_visualizar_iniciar_modelo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Añadir etiqueta con el titulo
        self.model_title = QLabel("View and start model")
        self.model_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout_visualizar_iniciar_modelo.addWidget(self.model_title)
        #Añadir etiqueta para el boton start model
        layout_boton_start = QGridLayout()
        self.model_button =  QPushButton("Start model")
        self.model_button.setFixedSize(135, 40)
        self.model_button.setEnabled(False)
        self.model_button.clicked.connect(self.start_model)
        layout_boton_start.addWidget(self.model_button)
        layout_boton_start.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_visualizar_iniciar_modelo.addLayout(layout_boton_start)
        # Añadir layout de la formula
        layout_visualizar_iniciar_modelo.addLayout(layout_graph_formula)
        # Añadir layout descripcion
        layout_visualizar_iniciar_modelo.addLayout(layout_descripcion_modelo)
        # Limites layout visualizar e iniciar modelo
        layout_visualizar_iniciar_modelo.setContentsMargins(0,20,0,20)
        

       
        
        
        
        
        
        # Layout botones guardar modelo y hacer prediccion
        layout_guardarmodelo_prediccion = QHBoxLayout()
        layout_guardarmodelo_prediccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Añadir boton guardar modelo
        self.save_button = QPushButton("Save Model")
        self.save_button.setFixedSize(135, 40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_model)
        layout_guardarmodelo_prediccion.addWidget(self.save_button)
        #Añadir boton prediccion
        self.predict_button = QPushButton("Make Prediction")
        self.predict_button.setFixedSize(135, 40)
        self.predict_button.setEnabled(False)  # Deshabilitado inicialmente
        self.predict_button.clicked.connect(self.make_prediction)
        layout_guardarmodelo_prediccion.addWidget(self.predict_button)

        

        
       
        #Layout mostrar prediccion
        layout_mostrar_prediccion = QVBoxLayout()
        layout_mostrar_prediccion.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Área de predicción
        self.prediction_area = QWidget()
        self.prediction_layout = QVBoxLayout()
        self.prediction_area.setLayout(self.prediction_layout)
        layout_mostrar_prediccion.addWidget(self.prediction_area)
        # Área para mostrar el resultado de la predicción
        self.result_label = QLabel("")
        layout_mostrar_prediccion.addWidget(self.result_label)
        

    
        # Creamos el layout principal y le añadimos los auxiliares
        layout = QVBoxLayout()
        layout.addLayout(self.d_u.layout)
        layout.addLayout(layout_entrada_salida_preprocesado)
        layout.addLayout(layout_visualizar_iniciar_modelo)
        layout.addLayout(layout_mostrar_prediccion)
        layout.addLayout(layout_guardarmodelo_prediccion)
    
    
        container = QWidget()
        container.setLayout(layout)
        
        # Crear un área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Desactiva el scroll horizontal
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Activa el scroll vertical solo si es necesario

        # Crear el diseño principal y añadir el área de scroll
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(scroll_area)
        
        # Configurar el diseño principal para la ventana
        self.setCentralWidget(main_widget)
    


   
   

    # Método para crear el modelo y mostrar la gráfica
    def start_model(self):
        # Limpiar campos de entrada anteriores antes de iniciar un nuevo modelo
        self.reset_input_fields()
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
                # Limpiar campos de entrada anteriores antes de iniciar un nuevo modelo
                self.reset_input_fields()
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
        self.prep_title.hide()
        self.model_title.hide()
        self.entrada_salida_titulo.hide()
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
        self.graph_widget.hide()
        self.label_formula.setVisible(True)
        self.label_r2_mse.setVisible(True)
        self.result_label.setVisible(False)

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
            self.input_labels[field_name] = input_label
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
            self.result_label.setVisible(True)
            if self.model_output == None:
                self.result_label.setText(f"Prediction result ({self.output_col}): {prediction[0]:.4f}")
            else:
                self.result_label.setText(f"Prediction result ({self.model_output}): {prediction[0]:.4f}")
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
    def reset_input_fields(self):
    # Eliminar todos los campos de entrada actuales
        for field in self.input_labels.values():
            field.deleteLater()
        for field in self.input_fields.values():
            field.deleteLater()
        self.input_fields.clear()
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