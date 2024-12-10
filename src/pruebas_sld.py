import unittest
from unittest.mock import MagicMock, patch
import joblib
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel, QLineEdit, QTextEdit
from SLD_funcs import SLDFuncs
from SLD_UI import SLDUI
from modelo_lineal import model
import numpy as np

class TestSLDFuncs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        # Crear datos de prueba para el modelo real
        x = np.array([[1], [2], [3], [4]])
        y = np.array([2, 4, 6, 8])
        self.model_instance, self.r2, self.mse = model(x, y)

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
        self.funcs.load_model()
        mock_dialog.assert_called_once()
        mock_load.assert_called_once()
        mock_msg.assert_called_once_with(None, "Load model", "The model has been loaded successfully.")

    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    def test_make_prediction_invalid_input(self, mock_warning):
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("abc")  # Entrada no válida

        self.funcs.make_prediction()
        mock_warning.assert_called_once_with(None, "Incorrect input", "could not convert string to float: 'abc'")

    def test_make_prediction_success(self):
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("5")  # Entrada válida

        self.funcs.make_prediction()
        result_text = self.funcs.result_label.text()
        self.assertIn("Prediction result", result_text)

    def test_reset_input_fields(self):
        self.funcs.input_fields = {"feature1": QLineEdit()}
        self.funcs.reset_input_fields()
        self.assertEqual(len(self.funcs.input_fields), 0)

class TestSLDUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.mock_model = MagicMock()
        self.ui = SLDUI(self.mock_model)

    def test_enable_prediction(self):
        self.ui.m_f.model = MagicMock()
        self.ui.enable_prediction()
        self.assertTrue(self.ui.predict_button.isEnabled())

    def test_generate_input_fields(self):
        self.ui.m_f.model.feature_names_in_ = ["feature1"]
        self.ui.generate_input_fields()
        self.assertIn("feature1", self.ui.funcs.input_fields)

if __name__ == "__main__":
    unittest.main()