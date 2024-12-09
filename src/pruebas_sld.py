import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel, QLineEdit
from SLD_funcs import SLDFuncs
from SLD_UI import SLDUI

class TestSLDFuncs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_model.model = MagicMock()
        self.mock_model.feature_names_in_ = ["feature1", "feature2"]
        self.mock_description = MagicMock()
        self.mock_result_label = QLabel()
        self.funcs = SLDFuncs(self.mock_model, self.mock_description, self.mock_result_label)

    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=("test_model.joblib", True))
    @patch('joblib.dump')
    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_save_model(self, mock_msg, mock_dump, mock_dialog):
        self.funcs.save_model()
        mock_dialog.assert_called_once()
        mock_dump.assert_called_once()
        mock_msg.assert_called_once_with(None, "Saved Successfully", "The model has been saved successfully.")

    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=("test_model.joblib", True))
    @patch('joblib.load', return_value={"model": MagicMock(), "input_columns": ["feature1", "feature2"]})
    @patch('PyQt6.QtWidgets.QMessageBox.information')
    def test_load_model(self, mock_msg, mock_load, mock_dialog):
        self.funcs.load_model()
        mock_dialog.assert_called_once()
        mock_load.assert_called_once()
        mock_msg.assert_called_once_with(None, "Load model", "The model has been loaded successfully.")

    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    @patch('PyQt6.QtWidgets.QMessageBox.critical')
    def test_make_prediction_invalid_input(self, mock_critical, mock_warning):
        self.funcs.input_fields = {"feature1": QLineEdit(), "feature2": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("")
        self.funcs.input_fields["feature2"].setText("5.5")

        self.funcs.make_prediction()
        mock_warning.assert_called_once_with(None, "Incorrect input", "Please enter a value for feature1")

    @patch('PyQt6.QtWidgets.QMessageBox.critical')
    def test_make_prediction_error(self, mock_critical):
        self.funcs.input_fields = {"feature1": QLineEdit(), "feature2": QLineEdit()}
        self.funcs.input_fields["feature1"].setText("abc")  # Invalid input
        self.funcs.input_fields["feature2"].setText("5.5")

        self.funcs.make_prediction()
        mock_critical.assert_called_once()

    def test_reset_input_fields(self):
        self.funcs.input_fields = {"feature1": QLineEdit(), "feature2": QLineEdit()}
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
        self.ui.m_f.model.feature_names_in_ = ["feature1", "feature2"]
        self.ui.generate_input_fields()
        self.assertIn("feature1", self.ui.funcs.input_fields)
        self.assertIn("feature2", self.ui.funcs.input_fields)

if __name__ == "__main__":
    unittest.main()