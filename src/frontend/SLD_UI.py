from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from backend.SLD_funcs import SLDFuncs


class SLDUI:
    """
    Clase que basada en describir un modelo, guardar el modelo 
    y realizar predicciones basadas en sus características.

    Atributos:
        layout (QVBoxLayout): Layout principal de la interfaz.
        m_f: Instancia de la clase MFuncs en model_func
        description_text (QTextEdit): Campo de texto para ingresar la descripción del modelo.
        result_label (QLabel): Etiqueta que muestra los resultados de las predicciones.
        predict_button (QPushButton): Botón para realizar predicciones.
        funcs (SLDFuncs): Clase de backend que administra las funciones del modelo y predicciones.
    """
    def __init__(self, model):
        """
        Inicializa una instancia de la clase SLDUI.

        Parámetros:
            model: Modelo de predicción que se utilizará en la interfaz.
        """
        self.layout = QVBoxLayout
        self.m_f = model
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText(
            "Add a description for the model...")
        self.result_label = QLabel("")
        self.predict_button = QPushButton("Make Prediction")
        self.funcs = SLDFuncs(
            self.m_f, self.description_text, self.result_label)
        self.inicializar()

    def inicializar(self):
        """
        Configura los elementos de la interfaz gráfica, incluyendo:
        - Área para ingresar una descripción opcional del modelo.
        - Botones para guardar el modelo y realizar predicciones.
        - Área para mostrar resultados de predicciones.
        """

        # Layout para la descripción del modelo
        self.description_layout = QVBoxLayout()
        self.description_area = QWidget()
        self.description_area.setFixedSize(1480,160)
        self.description_area.setContentsMargins(0,0,0,0)
        
        # Título de la descripción del modelo
        self.layout_descripcion_modelo = QVBoxLayout()
        self.description_label = QLabel("Model description (optional): ")
        self.description_label.setStyleSheet(
            "font-size: 18px; font-weight: bold;")
        self.description_text.setFixedSize(1495,100)
        
        self.layout_descripcion_modelo.addWidget(self.description_label)
        self.layout_descripcion_modelo.addWidget(self.description_text)
        self.description_area.setLayout(self.layout_descripcion_modelo)
        self.description_layout.addWidget(self.description_area)
        
        # Layout para los botones de guardar modelo y realizar predicciones
        self.layout_guardarmodelo_prediccion = QHBoxLayout()
        self.layout_guardarmodelo_prediccion.setAlignment(
            Qt.AlignmentFlag.AlignCenter)
        
        # Botón para guardar modelo
        self.save_button = QPushButton("Save Model")
        self.save_button.setFixedSize(135, 40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.funcs.save_model)
        self.layout_guardarmodelo_prediccion.addWidget(self.save_button)
        
        # Botón para realizar predicciones
        self.predict_button.setFixedSize(135, 40)
        self.predict_button.setEnabled(False)  # Deshabilitado inicialmente
        self.predict_button.clicked.connect(self.funcs.make_prediction)
        self.layout_guardarmodelo_prediccion.addWidget(self.predict_button)

        # Layout para mostrar las predicciones
        self.layout_mostrar_prediccion = QVBoxLayout()
        self.layout_mostrar_prediccion.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_mostrar_prediccion.setContentsMargins(0,0,0,0)
        # Área de predicción
        self.prediction_area = QWidget()
        self.prediction_layout = QVBoxLayout()
        self.prediction_area.setLayout(self.prediction_layout)
        self.layout_mostrar_prediccion.addWidget(self.prediction_area)
       
        # Etiqueta para mostrar el resultado de las predicciones
        self.layout_mostrar_prediccion.addWidget(self.result_label)

    def enable_prediction(self, ready = False):
        """
        Habilita el botón de predicción y genera los campos de entrada para
        realizar predicciones si un modelo está disponible.

        Parámetros:
            ready (bool, opcional): Indica si el modelo está listo para realizar predicciones.
                Valor por defecto: False.
        """
        if self.funcs.file_name or ready == True:
            if self.m_f.model or self.funcs.model:
                self.predict_button.setEnabled(True)
                self.generate_input_fields()

    def generate_input_fields(self):
        """
        Genera dinámicamente los campos de entrada según las variables de entrada del modelo.

        Para cada variable de entrada en el modelo, se crea un QLabel y un QLineEdit
        para que el usuario pueda ingresar los valores correspondientes.
        """
        for field_name in self.m_f.model.feature_names_in_:
            input_label = QLabel(f"Enter {field_name}:")
            input_field = QLineEdit()
            input_field.setFixedSize(200,30)
            self.prediction_layout.addWidget(input_label)
            self.prediction_layout.addWidget(input_field)
            self.prediction_layout.update()
            self.funcs.input_fields[field_name] = input_field
            self.funcs.input_labels[field_name] = input_label
