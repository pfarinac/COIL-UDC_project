from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from joblib import dump
from PyQt6.QtGui import QColor
from modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from data import Data

class Input_Output:
    def __init__(self) -> None:
        self._layout = QHBoxLayout()
        self.d = Data()
        
        self.inicializarUI()
    def inicializarUI(self):
            layout_entrad = QVBoxLayout()
            layout_salid = QVBoxLayout()



            self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout_entrad.setContentsMargins(0,20,20,20)
            layout_salid.setContentsMargins(20,20,0,20)

            # Selector para columnas de entrada (features)
            self.features_label = QLabel("Selecciona las columnas de entrada (features):")
            layout_entrad.addWidget(self.features_label)
            self.features_list = self.d.features_list
            self.features_list.setFixedSize(245, 60)
            self.features_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            layout_entrad.addWidget(self.features_list)
                
            # Selector único para la columna de salida
            self.target_label = QLabel("Selecciona la columna de salida (target):")
            layout_salid.addWidget(self.target_label)
            self.target_combo = self.d.target_combo
            self.target_combo.setFixedSize(215, 60)
            self.target_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            layout_salid.addWidget(self.target_combo)
            
            # Botón para confimar la selección de las columnas 
            self.confirm = QPushButton("Confirmar selección")
            self.confirm.setFixedSize(150, 25)
            self.input_col = [] # Lista con las columnas de entrada
            self.output_col = [] # Variable str que contiene la columna de salida
            self.features_list.clicked.connect(self.registrar_input)
            self.confirm.clicked.connect(self.almacenar)
            self._layout.addLayout(layout_entrad)
            self._layout.addLayout(layout_salid)
            self._layout.addWidget(self.confirm)

            # Función para registrar las columnas de entrada
    def registrar_input(self):

            input_col_text = self.features_list.currentItem().text()
            if input_col_text in self.input_col:
                self.input_col.remove(input_col_text)
            else:
                self.input_col.append(input_col_text)
                self.habilitar_botones_preprocesado(False)

    
    def habilitar_botones_preprocesado(self, habilitar):
            self.btn_count_nulls.setEnabled(habilitar)
            self.btn_remove_nulls.setEnabled(habilitar)
            self.btn_replace_nulls_mean.setEnabled(habilitar)
            self.btn_replace_nulls_median.setEnabled(habilitar)
            self.btn_replace_nulls_value.setEnabled(habilitar)


        # Función para almacenar las selecciones de las columnas e imprimir el mensaje por pantalla
    def almacenar(self):

            self.output_col = self.target_combo.currentItem().text()
            self.model_description = self.description_text.toPlainText()
            if self.output_col == [] or self.input_col == []:
                QMessageBox.warning(self,"Advertencia","Por favor seleccione al menos una columna de entrada y una de salida")
            else:
                message = "Tu seleccion se ha guardado correactamente.\n"
                QMessageBox.information(self,"Información", message)
                self.habilitar_botones_preprocesado(True)  

    def get_layout(self):
          return self._layout