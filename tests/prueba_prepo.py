import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from PyQt6.QtWidgets import QApplication
import sys
import os

# Agregar la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.prepro_func import PFuncs
from frontend.prepro_UI import PUI

class TestPFuncs(unittest.TestCase):
    """
    Clase de prueba unitaria para las funciones del preprocesado de datos de la clase PFuncs.
    Verifica el comportamiento de las funciones relacionadas con el manejo de valores nulos en los datos.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura la aplicación antes de ejecutar las pruebas.
        Inicializa una instancia de QApplication para las pruebas de la interfaz de usuario.
        """
        cls.app = QApplication([])

    def setUp(self):
        """
        Configura el entorno necesario para cada prueba.
        Crea una instancia mock de los datos y una instancia de PFuncs para las pruebas.
        """
        # Simular una clase de datos con atributos básicos
        self.mock_data = MagicMock()
        self.mock_data.df = pd.DataFrame({
            "Input1": [1, None, 3],
            "Input2": [None, 5, 6],
            "Output": [7, 8, None]
        })
        self.mock_data.input_col = ["Input1", "Input2"]
        self.mock_data.output_col = "Output"
        self.mock_data.table_widget = MagicMock()
        self.funcs = PFuncs(self.mock_data)

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_count_nulls(self, mock_info):
        """
        Prueba para verificar que el conteo de valores nulos en las columnas se realice correctamente.
        Verifica si se muestra el mensaje adecuado con el número de valores nulos por columna.
        """
        self.funcs.count_nulls()
        mock_info.assert_called_once_with(
            None, "Null values", "Number of null values ​​per column:\nInput1: 1\nInput2: 1\nOutput: 1"
        )
        self.assertFalse(self.funcs.no_nulls)

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_remove_nulls(self, mock_info):
        """
        Prueba para verificar que las filas con valores nulos sean eliminadas correctamente.
        Verifica que se muestre el mensaje adecuado con la cantidad de filas eliminadas.
        """
        original_rows = len(self.mock_data.df)
        self.funcs.remove_nulls()
        new_rows = len(self.mock_data.df)
        mock_info.assert_called_once_with(
            None, "Deleted Rows", f" {original_rows - new_rows} rows with null values in the selectd columns were deleted."
        )

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_replace_nulls_with_mean(self, mock_info):
        """
        Prueba para verificar que los valores nulos sean reemplazados por la media de las columnas seleccionadas.
        Verifica que los valores nulos sean reemplazados correctamente con la media y muestra el mensaje correspondiente.
        """
        self.funcs.replace_nulls_with_mean()
        # Verificar que los valores nulos fueron reemplazados
        self.assertEqual(self.mock_data.df["Input1"].iloc[1], 2.0)  # Media de Input1
        self.assertEqual(self.mock_data.df["Output"].iloc[2], 7.5)  # Media de Output
        mock_info.assert_called_once_with(
            None, "Replaced values", "Null values ​​have been replaced by the mean of the selected columns."
        )

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_replace_nulls_with_median(self, mock_info):
        """
        Prueba para verificar que los valores nulos sean reemplazados por la mediana de las columnas seleccionadas.
        Verifica que los valores nulos sean reemplazados correctamente con la mediana y muestra el mensaje correspondiente.
        """
        self.funcs.replace_nulls_with_median()
        # Verificar que los valores nulos fueron reemplazados
        self.assertEqual(self.mock_data.df["Input1"].iloc[1], 2.0)  # Mediana de Input1
        self.assertEqual(self.mock_data.df["Output"].iloc[2], 7.5)  # Mediana de Output
        mock_info.assert_called_once_with(
            None, "Replaced values", "Null values ​​have been replaced by the median of the selected columns."
        )

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    @patch('PyQt6.QtWidgets.QInputDialog.getText', return_value=("42", True))
    def test_replace_nulls_with_value(self, mock_input, mock_info):
        """
        Prueba para verificar que los valores nulos sean reemplazados por un valor especificado por el usuario.
        Simula la entrada de un valor y verifica que los valores nulos sean reemplazados correctamente.
        """
        self.funcs.replace_nulls_with_value()
        # Verificar que los valores nulos fueron reemplazados con el valor ingresado
        self.assertEqual(self.mock_data.df["Input1"].iloc[1], "42")
        self.assertEqual(self.mock_data.df["Output"].iloc[2], "42")
        mock_info.assert_called_once_with(
            None, "Replaced values", "Null values has been replaced by '42' in the selected columns."
        )

class TestPUI(unittest.TestCase):
    """
    Clase de prueba unitaria para la interfaz de usuario de preprocesado de datos (PUI).
    Verifica que los botones de la interfaz de usuario se habiliten correctamente según el estado de los datos.
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
        Crea una instancia mock de los datos y una instancia de la interfaz PUI.
        """
        self.mock_data = MagicMock()
        self.ui = PUI(self.mock_data)

    def test_habilitar_botones_preprocesado(self):
        """
        Prueba para verificar que los botones de preprocesado se habiliten correctamente
        cuando no haya valores nulos en los datos.
        """
        self.ui.funcs.no_nulls = False
        # Simular la habilitación de botones
        self.ui.habilitar_botones_preprocesado()
        self.assertTrue(self.ui.btn_remove_nulls.isEnabled())
        self.assertTrue(self.ui.btn_replace_nulls_mean.isEnabled())
        self.assertTrue(self.ui.btn_replace_nulls_median.isEnabled())
        self.assertTrue(self.ui.btn_replace_nulls_value.isEnabled())

if __name__ == "__main__":
    unittest.main()
