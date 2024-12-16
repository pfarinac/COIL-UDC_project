import unittest
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication, QLabel, QListWidget, QTableWidget
import pandas as pd
import sys
import os

# Agregar la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backend.data_func import Funcs

class TestFuncs(unittest.TestCase):
    """
    Pruebas unitarias para la clase Funcs.
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
        - Instancia un objeto Funcs con los widgets simulados.
        """
        self.target_combo = QListWidget()
        self.features_list = QListWidget()
        self.file_path_label = QLabel()
        self.table_widget = QTableWidget()

        self.funcs = Funcs(
            target_combo=self.target_combo,
            features_list=self.features_list,
            path=self.file_path_label,
            table=self.table_widget
        )

    @classmethod
    def tearDownClass(cls):
        """
        Limpieza final después de todas las pruebas.
        """
        cls.app.quit()

    def test_inicializacion(self):
        """
        Prueba que verifica la correcta inicialización de los atributos de la clase Funcs.
        """
        self.assertIsNone(self.funcs.df)
        self.assertEqual(self.funcs.input_col, [])
        self.assertIsInstance(self.funcs.target_combo, QListWidget)
        self.assertIsInstance(self.funcs.file_path_label, QLabel)

    @patch('pandas.read_csv')  # Mock para pandas.read_csv
    def test_load_file_csv(self, mock_read_csv):
        """
        Prueba la funcionalidad de cargar un archivo CSV:
        - Simula la selección de un archivo y la lectura del DataFrame.
        - Verifica que se llama al diálogo de archivo y que los datos se cargan correctamente.
        """
        mock_read_csv.return_value = pd.DataFrame({"Col1": [1, 2], "Col2": [3, 4]})
        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = ('test.csv', 'CSV Files (*.csv)')

            self.funcs.load_file()

            mock_dialog.assert_called_once()
            self.assertIsNotNone(self.funcs.df)
            self.assertEqual(self.funcs.df.shape, (2, 2))
            self.assertEqual(self.file_path_label.text(), 'File path: test.csv')

    def test_mostrar_columnas(self):
        """
        Prueba que las columnas de un DataFrame se muestren correctamente en los widgets:
        - Simula la carga de un DataFrame.
        - Verifica que las columnas aparecen en los widgets `features_list` y `target_combo`.
        """
        self.funcs.df = pd.DataFrame({"Col1": [1, 2], "Col2": [3, 4]})
        self.funcs.mostrar_columnas()

        self.assertEqual(self.features_list.count(), 2)
        self.assertEqual(self.target_combo.count(), 2)

    def test_update_table(self):
        """
        Prueba la actualización de una tabla con un DataFrame:
        - Simula un DataFrame con valores nulos.
        - Verifica que las filas, columnas y contenido de la tabla se actualizan correctamente.
        """
        df = pd.DataFrame({"Col1": [1, None], "Col2": [3, 4]})
        self.funcs.update_table(self.table_widget, df)

        self.assertEqual(self.table_widget.rowCount(), 2)
        self.assertEqual(self.table_widget.columnCount(), 2)
        self.assertEqual(self.table_widget.horizontalHeaderItem(0).text(), "Col1")
        self.assertEqual(self.table_widget.horizontalHeaderItem(1).text(), "Col2")

        self.assertEqual(self.table_widget.item(0, 0).text(), "1.0")
        self.assertEqual(self.table_widget.item(1, 0).background().color().name(), "#ff0000")  # Color rojo

    def test_registrar_input(self):
        """
        Prueba la funcionalidad de registrar una columna seleccionada como entrada:
        - Simula la selección y deselección de columnas.
        - Verifica que las columnas se agregan o eliminan correctamente de `input_col`.
        """
        self.features_list.addItem("Col1")
        self.features_list.setCurrentRow(0)
        self.funcs.registrar_input()

        self.assertIn("Col1", self.funcs.input_col)

        self.funcs.registrar_input()
        self.assertNotIn("Col1", self.funcs.input_col)

    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    def test_almacenar_warning(self, mock_warning):
        """
        Prueba el comportamiento de 'almacenar' cuando no se han seleccionado entradas ni salidas:
        - Verifica que se muestra un mensaje de advertencia al usuario.
        """
        self.funcs.almacenar()
        mock_warning.assert_called_once_with(
            None, "Warning", "Please select at least an input and an output column"
        )

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_almacenar_success(self, mock_info):
        """
        Prueba el comportamiento de 'almacenar' cuando se realiza una selección válida:
        - Simula la selección de columnas de entrada y salida.
        - Verifica que se muestra un mensaje de confirmación al usuario.
        """
        self.features_list.addItem("Input")
        self.target_combo.addItem("Output")
        self.funcs.input_col = ["Input"]
        self.funcs.target_combo.setCurrentRow(0)

        self.funcs.almacenar()
        mock_info.assert_called_once_with(
            None, "Information", "Your selection has been successfully saved.\n"
        )

if __name__ == '__main__':
    unittest.main()
