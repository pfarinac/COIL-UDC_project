from PyQt6.QtWidgets import (QPushButton, QFileDialog, QLabel, QMessageBox)
import joblib
from joblib import dump
from backend.modelo_lineal import model
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class SLDFuncs:
    def __init__(self, m_f, description_text: QTextEdit, result_label: QLabel, predict_button=QPushButton) -> None:
        self.m_f = m_f
        self.description_text = description_text
        self.result_label = result_label
        self.predict_button = predict_button
        self.input_fields = {}
        self.input_labels = {}
        self.file_name = None

    def save_model(self):
        self.update_model()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save model", "", "Joblib Files (*.joblib)")

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
                QMessageBox.information(
                    None, "Saved Successfully", "The model has been saved successfully.")
            except Exception as e:
                QMessageBox.critical(
                    None, "Error", f"Could not save model: {str(e)}")

    def load_model(self):
        # Abrir el diálogo de selección de archivo
        self.file_name, _ = QFileDialog.getOpenFileName(
            None, "Load model", "", "Model Files (*.pkl *.joblib)")

        if self.file_name:
            try:
                # Limpiar campos de entrada anteriores antes de iniciar un nuevo modelo
                self.reset_input_fields()
                # Cargar el modelo desde el archivo
                self.loaded_model_data = joblib.load(self.file_name)
                # Actualizar la interfaz con la información del modelo cargado
                self.loaded_model(self.loaded_model_data)
                # Mostrar mensaje de confirmación de carga
                QMessageBox.information(
                    None, "Load model", "The model has been loaded successfully.")
            except Exception as e:
                # Mostrar mensaje de error si el archivo es inválido
                QMessageBox.warning(None, "Error Loading Model",
                                    f"Could not load model: {str(e)}")

    def make_prediction(self):
        self.update_model()
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
                self.result_label.setText(
                    f"Prediction result ({self.output_col}): {prediction[0]:.4f}")
            else:
                self.result_label.setText(
                    f"Prediction result ({self.model_output}): {prediction[0]:.4f}")
        except ValueError as ve:
            QMessageBox.warning(None, "Incorrect input", str(ve))
        except Exception as e:
            QMessageBox.critical(None, "Prediction error",
                                 f"Error during prediction: {e}")

    def reset_input_fields(self):
        # Eliminar todos los campos de entrada actuales
        for field in self.input_labels.values():
            field.deleteLater()
        for field in self.input_fields.values():
            field.deleteLater()
        self.input_fields.clear()

    def loaded_model(self, model_data):
        # Cargar los datos del modelo cargado
        if "model" in model_data:
            self.model = model_data["model"]
            self.model_input = model_data["input_columns"]
            self.model_output = model_data["output_column"]
            self.r2_score = model_data.get("r2_score", "N/A")
            self.mse = model_data.get("mse", "N/A")
            self.description = model_data.get(
                "description", "No description available.")
            self.m_f.model = self.model
            self.m_f.model_input = self.model_input
            self.m_f.model_output = self.model_output
            self.m_f.r2 = self.r2_score
            self.m_f.mse = self.mse
            self.m_f.output_col = self.model_output

    def update_model(self):
        self.model = self.m_f.model
        self.model_input = self.m_f.model_input
        self.model_output = self.m_f.model_output
        self.r2 = self.m_f.r2
        self.mse = self.m_f.mse
        self.output_col = self.m_f.output_col
