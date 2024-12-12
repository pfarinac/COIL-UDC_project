from PyQt6.QtWidgets import (QPushButton, QFileDialog, QLabel, QMessageBox)
import joblib
from joblib import dump
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class SLDFuncs:
    """
    Clase que proporciona funcionalidades para guardar, cargar y usar un modelo, añadir una descripción al modelo,
    incluyendo realizar predicciones y gestionar la interfaz de usuario asociada.
    """

    def __init__(self, m_f, description_text: QTextEdit, result_label: QLabel, predict_button=QPushButton) -> None:
        """
        Inicializa una instancia de la clase SLDFuncs.

        Parámetros:
            m_f: Instancia de MFuncs.
            description_text (QTextEdit): Campo de texto para la descripción del modelo.
            result_label (QLabel): Etiqueta para mostrar el resultado de las predicciones.
            predict_button (QPushButton): Botón para activar predicciones.
        """
        self.m_f = m_f
        self.description_text = description_text
        self.result_label = result_label
        self.predict_button = predict_button
        self.input_fields = {}
        self.input_labels = {}
        self.file_name = None

    def save_model(self):
        """
        Guarda el modelo entrenado junto con su configuración en un archivo.
        Solicita al usuario seleccionar una ubicación de guardado y gestiona posibles errores.
        """
        self.update_model()

        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save model", "", "Joblib Files (*.joblib)")

        if not file_path:

            QMessageBox.warning(
                None, "Warning", "No file path selected. The model was not saved.")
            return

        model_data = {
            "model": self.model,
            "description": self.description_text.toPlainText(),
            "input_columns": self.model_input,
            "output_column": self.model_output,
            "r2_score": self.r2,
            "mse": self.mse
        }

        try:

            joblib.dump(model_data, file_path)

            QMessageBox.information(
                None, "Saved Successfully", "The model has been saved successfully.")
        except Exception as e:

            QMessageBox.critical(
                None, "Error", f"Could not save model: {str(e)}")

    def load_model(self):
        """
        Carga un modelo guardado desde un archivo. Actualiza la interfaz y los campos relacionados.
        Muestra mensajes de error si el archivo no es válido.
        """
        self.file_name, _ = QFileDialog.getOpenFileName(
            None, "Load model", "", "Model Files (*.pkl *.joblib)")

        if self.file_name:
            try:

                self.reset_input_fields()

                self.loaded_model_data = joblib.load(self.file_name)

                self.loaded_model(self.loaded_model_data)

                QMessageBox.information(
                    None, "Load model", "The model has been loaded successfully.")
            except Exception as e:

                QMessageBox.warning(None, "Error Loading Model",
                                    f"Could not load model: {str(e)}")

    def make_prediction(self):
        """
        Realiza una predicción utilizando el modelo cargado o creado. Muestra los resultados
        en la interfaz de usuario. Gestiona errores relacionados con entradas inválidas.
        """
        self.update_model()
        try:
            input_values = []
            for field_name, input_field in self.input_fields.items():
                value = input_field.text()
                if value == "":
                    raise ValueError(f"Please enter a value for {field_name}")
                input_values.append(float(value))

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
        """
        Elimina los campos de entrada y etiquetas actuales de la interfaz.
        """
        for field in self.input_labels.values():
            field.deleteLater()
        for field in self.input_fields.values():
            field.deleteLater()
        self.input_fields.clear()

    def loaded_model(self, model_data):
        """
        Actualiza la configuración del modelo y la interfaz de usuario con los datos de un modelo cargado.

        Parámetros:
            model_data (dict): Datos cargados del modelo guardado.
        """
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
        """
        Actualiza las propiedades del modelo y sus configuraciones desde la instancia asociada.
        """
        self.model = self.m_f.model
        self.model_input = self.m_f.model_input
        self.model_output = self.m_f.model_output
        self.r2 = self.m_f.r2
        self.mse = self.m_f.mse
        self.output_col = self.m_f.output_col
