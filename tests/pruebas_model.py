import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.model_func import MFuncs

class TestMFuncs(unittest.TestCase):
    """
    Conjunto de pruebas para la clase MFuncs.
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
        """
        self.mock_data = MagicMock()
        self.mock_figure = Figure()
        self.mock_canvas = MagicMock(spec=FigureCanvas)
        self.label_formula = QLabel()
        self.label_r2_mse = QLabel()
        self.funcs = MFuncs(self.mock_data, self.mock_figure, self.mock_canvas, self.label_formula, self.label_r2_mse)

    @classmethod
    def tearDownClass(cls):
        """
        Limpia la instancia de QApplication después de completar todas las pruebas.
        """
        cls.app.quit()

    def test_inicializacion(self):
        """
        Prueba que la instancia de MFuncs se inicializa con los atributos correctos.
        """
        self.assertEqual(self.funcs.d_f, self.mock_data)
        self.assertIs(self.funcs.figure, self.mock_figure)
        self.assertIs(self.funcs.canvas, self.mock_canvas)
        self.assertIs(self.funcs.label_formula, self.label_formula)
        self.assertIs(self.funcs.label_r2_mse, self.label_r2_mse)

    def test_start_model_valid(self):
        """
        Prueba el método start_model cuando se proporcionan columnas de entrada y salida válidas.
        """
        self.funcs.df = MagicMock()
        self.funcs.input_col = ["col1"]
        self.funcs.output_col = "col2"
        with patch("backend.model_func.MFuncs.create_model") as mock_model:
            mock_clf = MagicMock()
            mock_model.return_value = (mock_clf, 0.95, 0.05)

            self.funcs.start_model()

            mock_model.assert_called_once_with(
                self.funcs.df[self.funcs.input_col],
                self.funcs.df[self.funcs.output_col]
            )
            self.assertTrue(self.label_formula.isVisible())
            self.assertTrue(self.label_r2_mse.isVisible())
            self.mock_canvas.draw.assert_called_once()

    def test_start_model_invalid(self):
        """
        Prueba el método start_model cuando se proporcionan columnas de entrada o salida inválidas.
        """
        self.funcs.d_f.df = None
        self.funcs.df = None
        self.funcs.input_col = []
        self.funcs.output_col = None

        with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning, \
             patch("backend.model_func.MFuncs.create_model") as mock_model:

            mock_model.side_effect = RuntimeError("model should not be called")
            mock_clf = MagicMock()
            mock_clf.coef_ = [0]
            mock_clf.intercept_ = 0
            mock_model.return_value = (mock_clf, None, None)

            self.funcs.start_model()

            mock_warning.assert_called_once_with(
                None, "Error", "The loaded data is incorrect, make sure you selected it correctly"
            )

            mock_model.assert_not_called()

    def test_formula(self):
        """
        Prueba el método formula para asegurar que genera la representación correcta de la ecuación del modelo.
        """
        self.funcs.model = MagicMock()
        self.funcs.model.coef_ = [2.5]
        self.funcs.model.intercept_ = 1.0
        result = self.funcs.formula(["x"], "y")
        self.assertEqual(result, "y = x  *  2.5  +   1.0")

    def test_update_input_output(self):
        """
        Prueba que update_input_output actualiza correctamente las columnas de entrada y salida desde la fuente de datos.
        """
        self.mock_data.input_col = ["col1"]
        self.mock_data.output_col = ["col2"]
        self.funcs.update_input_output()
        self.assertEqual(self.funcs.input_col, ["col1"])
        self.assertEqual(self.funcs.output_col, ["col2"])

    def test_update_df(self):
        """
        Prueba que update_df actualiza correctamente el dataframe desde la fuente de datos.
        """
        self.mock_data.df = MagicMock()
        self.funcs.update_df()
        self.assertEqual(self.funcs.df, self.mock_data.df)

if __name__ == '__main__':
    unittest.main()


