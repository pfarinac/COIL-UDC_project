import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QLabel, QMessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from model_func import MFuncs

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
        with patch("model_func.MFuncs.create_model") as mock_model:
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
        # Simular un DataFrame vacío o sin configuraciones válidas
        self.funcs.d_f.df = None
        self.funcs.df = None
        self.funcs.input_col = []
        self.funcs.output_col = None

        # Mockear QMessageBox.warning para capturar advertencias
        with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning, \
            patch("model_func.MFuncs.create_model") as mock_model:

            mock_model.side_effect = RuntimeError("model should not be called")
            # Simular un modelo con los atributos necesarios pero que no se usará
            mock_clf = MagicMock()
            mock_clf.coef_ = [0]  # Valores dummy
            mock_clf.intercept_ = 0
            mock_model.return_value = (mock_clf, None, None)

            # Llamar al método bajo prueba
            self.funcs.start_model()

            # Verificar que se muestra la advertencia
            mock_warning.assert_called_once_with(
                None, "Error", "The loaded data is incorrect, make sure you selected it correctly"
            )

            # Verificar que no se utilizó el modelo
            mock_model.assert_not_called()

    def test_formula(self):
        self.funcs.model = MagicMock()
        self.funcs.model.coef_ = [2.5]
        self.funcs.model.intercept_ = 1.0
        result = self.funcs.formula(["x"], "y")
        self.assertEqual(result, "y = x  *  2.5  +   1.0")

    def test_update_input_output(self):
        self.mock_data.input_col = ["col1"]
        self.mock_data.output_col = "col2"
        self.funcs.update_input_output()
        self.assertEqual(self.funcs.input_col, ["col1"])
        self.assertEqual(self.funcs.output_col, "col2")

    def test_update_df(self):
        self.mock_data.df = MagicMock()
        self.funcs.update_df()
        self.assertEqual(self.funcs.df, self.mock_data.df)

if __name__ == '__main__':
    unittest.main()

