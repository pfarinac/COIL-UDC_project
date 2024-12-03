
import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from model_UI import MUI
from model_func import MFuncs
from modelo_lineal import *

class TestMUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.mock_data = MagicMock()
        self.mui = MUI(self.mock_data)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def test_inicializacion(self):
        self.assertIsInstance(self.mui.layout, QVBoxLayout)
        self.assertIsInstance(self.mui.figure, Figure)
        self.assertIsInstance(self.mui.canvas, FigureCanvas)
        self.assertIsInstance(self.mui.label_formula, QLabel)
        self.assertIsInstance(self.mui.label_r2_mse, QLabel)

    def test_button_start_model(self):
        with patch.object(self.mui.funcs, "start_model") as mock_start_model:
            self.assertFalse(self.mui.model_button.isEnabled())
            self.mui.model_button.click()
            mock_start_model.assert_not_called()  # Mock method should not be called without data.

class TestMFuncs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.mock_data = MagicMock()
        self.mock_figure = Figure()
        self.mock_canvas = MagicMock(spec=FigureCanvas)
        self.label_formula = QLabel()
        self.label_r2_mse = QLabel()
        self.funcs = MFuncs(self.mock_data, self.mock_figure, self.mock_canvas, self.label_formula, self.label_r2_mse)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def test_inicializacion(self):
        self.assertEqual(self.funcs.d_f, self.mock_data)
        self.assertIs(self.funcs.figure, self.mock_figure)
        self.assertIs(self.funcs.canvas, self.mock_canvas)
        self.assertIs(self.funcs.label_formula, self.label_formula)
        self.assertIs(self.funcs.label_r2_mse, self.label_r2_mse)

    def test_start_model_valid(self):
        self.funcs.df = MagicMock()
        self.funcs.input_col = ["col1"]
        self.funcs.output_col = "col2"
        with patch("model_func.model") as mock_model:
            mock_model.return_value = (MagicMock(), 0.95, 0.05)
            self.funcs.start_model()
            self.assertTrue(self.label_formula.isVisible())
            self.assertTrue(self.label_r2_mse.isVisible())
            self.mock_canvas.draw.assert_called_once()

    def test_start_model_invalid(self):
        self.funcs.df = None
        self.funcs.input_col = []
        self.funcs.output_col = None
        with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning:
            self.funcs.start_model()
            mock_warning.assert_called_once()

    def test_formula(self):
        self.funcs.model = MagicMock()
        self.funcs.model.coef_ = [2.5]
        self.funcs.model.intercept_ = 1.0
        result = self.funcs.formula(["x"], "y")
        self.assertEqual(result, "y = x  *  2.5  +   1.0")

    def test_start_model_valid(self):
        # Simular un DataFrame
        self.funcs.df = MagicMock()
        self.funcs.input_col = ["col1"]
        self.funcs.output_col = "col2"
        self.funcs.df[self.funcs.input_col] = MagicMock()
        self.funcs.df[self.funcs.output_col] = MagicMock()

        
        # Mockear la función model
        with patch("modelo_lineal.model") as mock_model:
            # Crear un mock para el modelo
            mock_clf = MagicMock()
            mock_model.return_value = (mock_clf, 0.95, 0.05)  # clf, r2, mse

            # Llamar al método bajo prueba
            self.funcs.start_model()

            # Verificar comportamiento
            mock_model.assert_called_once_with(
                self.funcs.df[self.funcs.input_col],
                self.funcs.df[self.funcs.output_col]
            )
            self.assertTrue(self.label_formula.isVisible())
            self.assertTrue(self.label_r2_mse.isVisible())
            self.mock_canvas.draw.assert_called_once()
if __name__ == '__main__':
    unittest.main()
