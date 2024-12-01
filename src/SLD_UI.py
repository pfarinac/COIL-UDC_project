from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QTextEdit)
from PyQt6.QtCore import Qt

from modelo_lineal import model
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from SLD_funcs import *


class SLDUI:
    def __init__(self, model):
        self.layout = QVBoxLayout
        self.m_f = model
        self.description_text = QTextEdit()
        self.description_text.setFixedSize(1485,150)
        self.description_text.setContentsMargins(0,0,0,0)
        self.description_text.setPlaceholderText(
            "Add a description for the model...")
        self.result_label = QLabel("")
        self.predict_button = QPushButton("Make Prediction")
        self.funcs = SLDFuncs(
            self.m_f, self.description_text, self.result_label)
        self.inicializar()

    def inicializar(self):
        # Layout decripcion del modelo
        self.layout_descripcion_modelo = QVBoxLayout()
        self.layout_descripcion_modelo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Añadir etiqueta con el titulo
        self.description_label = QLabel("Model description (optional): ")
        self.description_label.setStyleSheet(
            "font-size: 18px; font-weight: bold;")
        self.layout_descripcion_modelo.addWidget(self.description_label)
        # Añadir etiqueta para escribir descripcion

        self.layout_descripcion_modelo.addWidget(self.description_text)

        # Layout botones guardar modelo y hacer prediccion
        self.layout_guardarmodelo_prediccion = QHBoxLayout()
        self.layout_guardarmodelo_prediccion.setAlignment(
            Qt.AlignmentFlag.AlignCenter)
        # Añadir boton guardar modelo
        self.save_button = QPushButton("Save Model")
        self.save_button.setFixedSize(135, 40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.funcs.save_model)
        self.layout_guardarmodelo_prediccion.addWidget(self.save_button)
        # Añadir boton prediccion

        self.predict_button.setFixedSize(135, 40)
        self.predict_button.setEnabled(False)  # Deshabilitado inicialmente
        self.predict_button.clicked.connect(self.funcs.make_prediction)
        self.layout_guardarmodelo_prediccion.addWidget(self.predict_button)

        # Layout mostrar prediccion
        self.layout_mostrar_prediccion = QVBoxLayout()
        self.layout_mostrar_prediccion.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Área de predicción
        self.prediction_area = QWidget()
        self.prediction_layout = QVBoxLayout()
        self.prediction_area.setLayout(self.prediction_layout)
        self.layout_mostrar_prediccion.addWidget(self.prediction_area)
        # Área para mostrar el resultado de la predicción

        self.layout_mostrar_prediccion.addWidget(self.result_label)

    def enable_prediction(self):
        # Habilita la funcionalidad de predicción cuando un modelo está disponible
        if self.m_f.model or self.funcs.model:
            self.predict_button.setEnabled(True)
            self.generate_input_fields()

    def generate_input_fields(self):
        # Genera campos de entrada dinámicos basados en las variables de entrada del modelo
        for field_name in self.m_f.model.feature_names_in_:
            input_label = QLabel(f"Enter {field_name}:")
            input_field = QLineEdit()
            self.prediction_layout.addWidget(input_label)
            self.prediction_layout.addWidget(input_field)
            self.prediction_layout.update()
            self.funcs.input_fields[field_name] = input_field
            self.funcs.input_labels[field_name] = input_label
