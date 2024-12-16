import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit
import numpy as np
import sys
import os

# Agregar la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.SLD_funcs import SLDFuncs
from frontend.SLD_UI import SLDUI
from backend.model_func import MFuncs


class TestSLDFuncs(unittest.TestCase):
    """
    Clase de pruebas unitarias para probar la funcionalidad de la clase SLDFuncs.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura una instancia de QApplication requerida para probar componentes de PyQt6.
        """
        cls.app = QApplication([])

    def setUp(self):
        """
        Configura los objetos y datos necesarios antes de cada prueba.
        Crea un modelo simulado, sus datos, y la instancia de SLDFuncs.
        """
        # Crear datos de prueba para el modelo real
        x = np.array([[1], [2], [3], [4]])
        y = np.array([2, 4, 6, 8])
        data_mock = MagicMock()  # Reemplazar con datos reales si es necesario
        figure_mock = MagicMock()
        canvas_mock = MagicMock()
        label_formula_mock = QLabel("Formula Label")
        label_r2_mse_mock = QLabel("R2/MSE Label")
        model_funcs_instance = MFuncs(data_mock, figure_mock, canvas_mock, label_formula_mock, label_r2_mse_mock)

        self.model_instance, self.r2, self.mse = model_funcs_instance.create_model(x, y)

        self.mock_model = MagicMock()
        self.description_text = QTextEdit()
        self.description_text.setPlainText("Test description")  # Asignar texto real
        self.mock_result_label = QLabel()
        self.mock_model.model = self.model_instance
        self.mock_model.feature_names_in_ = ["feature1"]
        self.mock_model.model_input = ["feature1"]
        self.mock_model.model_output = "target"
        self.mock_model.r2 = self.r2
        self.mock_model.mse = self.mse

        self.funcs = SLDFuncs(self.mock_model, self.description_text, self.mock_result_label)

    @patch('joblib.dump')  # Mock joblib.dump en el espacio de nombres correcto
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=("test_model.joblib", True))
    @patch('PyQt6.QtWidgets.QMessageBox.information')  # Mock QMessageBox.information
    def test_save_model(self, mock_msg, mock_file_dialog, mock_dump):
        """
        Test para verificar el comportamiento de la función `save_model` de SLDFuncs.
        Verifica que los datos se guarden correctamente y que se muestre un mensaje de éxito.
        """
        self.funcs.save_model()

        # Verificar si QFileDialog.getSaveFileName fue llamado
        mock_file_dialog.assert_called_once()

        # Verificar si joblib.dump fue llamado con los datos correctos
        expected_model_data = {
            "model": self.model_instance,
            "description": "Test description",  # Ahora es un string, no un mock
            "input_columns": ["feature1"],
            "output_column": "target",
            "r2_score": self.r2,
            "mse": self.mse
        }
        mock_dump.assert_called_once_with(expected_model_data, "test_model.joblib")  # Verifica la llamada

        # Verificar que se mostró un mensaje de éxito
        mock_msg.assert_called_once_with(None, "Saved Successfully", "The model has been saved successfully.")

    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=("test_model.joblib", True))
    @patch('joblib.load', return_value={
        "model": MagicMock(),
        "input_columns": ["feature1"],
        "output_column": "target",
        "r2_score": 0.95,
        "mse": 0.02,
        "description": "Test model"
    })
    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_load_model(self, mock_msg, mock_load, mock_dialog):
        """
        Test para verificar que el modelo se carga correctamente desde un archivo,
        y se muestra el mensaje de éxito.
        """
        self.funcs.load_model()
        mock_dialog.assert_called_once()
        mock_load.assert_called_once()
        mock_msg.assert_called_once_with(None, "Load model", "The model has been loaded successfully.")

    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    def test_make_prediction_invalid_input(self, mock_warning):
        """
        Test para verificar que se maneja correctamente una entrada inválida
        (en este caso, una cadena no convertible a float).
        """
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("abc")  # Entrada no válida

        self.funcs.make_prediction()
        mock_warning.assert_called_once_with(None, "Incorrect input", "could not convert string to float: 'abc'")

    def test_make_prediction_success(self):
        """
        Test para verificar que la predicción se realiza correctamente con una entrada válida.
        """
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("5")  # Entrada válida

        self.funcs.make_prediction()
        result_text = self.funcs.result_label.text()
        self.assertIn("Prediction result", result_text)

    def test_reset_input_fields(self):
        """
        Test para verificar que los campos de entrada se resetean correctamente.
        """
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.reset_input_fields()
        self.assertEqual(len(self.funcs.input_fields), 0)


class TestSLDUI(unittest.TestCase):
    """
    Clase de pruebas unitarias para probar la interfaz de usuario SLDUI.
    Verifica la habilitación de predicciones y la generación de campos de entrada dinámicamente.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura la aplicación de Qt para las pruebas.
        """
        cls.app = QApplication([])

    def setUp(self):
        """
        Configura los objetos y datos necesarios antes de cada prueba.
        Crea un modelo simulado y la instancia de SLDUI.
        """
        self.mock_model = MagicMock()
        self.ui = SLDUI(self.mock_model)

    def test_enable_prediction(self):
        """
        Test para verificar que el botón de predicción se habilite correctamente 
        cuando el modelo está listo.
        """
        self.ui.m_f.model = MagicMock()
        self.ui.enable_prediction(ready=True)
        self.assertTrue(self.ui.predict_button.isEnabled())

    def test_generate_input_fields(self):
        """
        Test para verificar que se generen correctamente los campos de entrada.
        """
        self.ui.m_f.model.feature_names_in_ = ["feature1"]
        self.ui.generate_input_fields()
        self.assertIn("feature1", self.ui.funcs.input_fields)

if __name__ == "__main__":
    unittest.main()
