import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QLabel, QListWidget, QTableWidget, QMessageBox
import pandas as pd
from data_func import Funcs  # Reemplaza "module_name" con el nombre del archivo de tu módulo.

class TestFuncs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear una instancia de QApplication antes de cualquier prueba
        cls.app = QApplication([])

    def setUp(self):
        # Crear elementos de UI simulados
        self.target_combo = QListWidget()
        self.features_list = QListWidget()
        self.file_path_label = QLabel()
        self.table_widget = QTableWidget()

        # Crear instancia de la clase Funcs
        self.funcs = Funcs(
            target_combo=self.target_combo,
            features_list=self.features_list,
            path=self.file_path_label,
            table=self.table_widget
        )

    @classmethod
    def tearDownClass(cls):
        # Cerrar la aplicación al finalizar las pruebas
        cls.app.quit()

    def test_inicializacion(self):
        # Verificar la inicialización de atributos
        self.assertIsNone(self.funcs.df)
        self.assertEqual(self.funcs.input_col, [])
        self.assertIsInstance(self.funcs.target_combo, QListWidget)
        self.assertIsInstance(self.funcs.file_path_label, QLabel)

    @patch('pandas.read_csv')  # Mock para pandas.read_csv
    def test_load_file_csv(self, mock_read_csv):
        # Simular DataFrame y QFileDialog
        mock_read_csv.return_value = pd.DataFrame({"Col1": [1, 2], "Col2": [3, 4]})
        with patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName') as mock_dialog:
            mock_dialog.return_value = ('test.csv', 'CSV Files (*.csv)')

            self.funcs.load_file()

            # Verificar que se llamó a QFileDialog
            mock_dialog.assert_called_once()
            # Verificar que se cargó el DataFrame correctamente
            self.assertIsNotNone(self.funcs.df)
            self.assertEqual(self.funcs.df.shape, (2, 2))
            self.assertEqual(self.file_path_label.text(), 'File path: test.csv')

    def test_mostrar_columnas(self):
        # Simular un DataFrame cargado
        self.funcs.df = pd.DataFrame({"Col1": [1, 2], "Col2": [3, 4]})
        self.funcs.mostrar_columnas()

        # Verificar que las columnas se añadieron a los widgets
        self.assertEqual(self.features_list.count(), 2)
        self.assertEqual(self.target_combo.count(), 2)

    def test_update_table(self):
        # Simular un DataFrame
        df = pd.DataFrame({"Col1": [1, None], "Col2": [3, 4]})
        self.funcs.update_table(self.table_widget, df)

        # Verificar el número de filas y columnas en la tabla
        self.assertEqual(self.table_widget.rowCount(), 2)
        self.assertEqual(self.table_widget.columnCount(), 2)
        self.assertEqual(self.table_widget.horizontalHeaderItem(0).text(), "Col1")
        self.assertEqual(self.table_widget.horizontalHeaderItem(1).text(), "Col2")

        # Verificar que las celdas contienen los valores correctos
        self.assertEqual(self.table_widget.item(0, 0).text(), "1.0")
        self.assertEqual(self.table_widget.item(1, 0).background().color().name(), "#ff0000")  # Color rojo

    def test_registrar_input(self):
        # Simular selección en la lista de características
        self.features_list.addItem("Col1")
        self.features_list.setCurrentRow(0)
        self.funcs.registrar_input()

        # Verificar que la columna se añadió a la lista de entrada
        self.assertIn("Col1", self.funcs.input_col)

        # Verificar comportamiento al deseleccionar
        self.funcs.registrar_input()
        self.assertNotIn("Col1", self.funcs.input_col)

    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    def test_almacenar_warning(self, mock_warning):
        # Simular condición en la que no hay selecciones
        self.funcs.almacenar()
        mock_warning.assert_called_once_with(
            None, "Warning", "Please select at least an input and an output column"
        )

    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_almacenar_success(self, mock_info):
        # Simular una selección válida
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
