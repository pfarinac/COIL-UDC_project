from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QGridLayout,
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from PyQt6.QtGui import QFont    
from data_func import *  
from prepro_func import *


class PUI:
    def __init__(self, data) -> None:
        self.layout = QVBoxLayout
        self.d_f = data
        self.funcs = PFuncs(self.d_f)
        self.inicializar()
        
    def inicializar(self):
        
        

        # Layout secundario preprocesado
        self.layout_preprocesado = QVBoxLayout()
        self.layout_preprocesado.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout_preprocesado.setContentsMargins(5, 20, 0, 0) 

        layout_count_nulls = QGridLayout()

        # Añadir etiqueta con el titulo
        self.prep_title = QLabel("Data preprocessing")
        self.prep_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout_preprocesado.addWidget(self.prep_title)

        #layout_count_nulls.addWidget(self.btn_count_nulls)
        layout_count_nulls.setContentsMargins(0,7,0,0)
        self.layout_preprocesado.addLayout(layout_count_nulls)
        
        # Layout resto de botones para nulos
        layout_nulls_buttons = QGridLayout()
        # Eliminar filas con nulos
        self.btn_remove_nulls = QPushButton("Delete rows with nulls")
        self.btn_remove_nulls.setFixedSize(320, 40)
        self.btn_remove_nulls.setEnabled(False)
        self.btn_remove_nulls.clicked.connect(self.funcs.remove_nulls)
        layout_nulls_buttons.addWidget(self.btn_remove_nulls, 0, 0)
        # Reemplazar nulos por media
        self.btn_replace_nulls_mean = QPushButton("Replace nulls with mean")
        self.btn_replace_nulls_mean.setFixedSize(320, 40)
        self.btn_replace_nulls_mean.setEnabled(False)
        self.btn_replace_nulls_mean.clicked.connect(self.funcs.replace_nulls_with_mean)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_mean, 0, 1)
        # Reemplazar nulos por mediana
        self.btn_replace_nulls_median = QPushButton("Replace nulls with median")
        self.btn_replace_nulls_median.setFixedSize(320, 40)
        self.btn_replace_nulls_median.setEnabled(False)
        self.btn_replace_nulls_median.clicked.connect(self.funcs.replace_nulls_with_median)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_median, 1,0)
        # Reemplazar nulos por un valor específico
        self.btn_replace_nulls_value = QPushButton("Replace nulls with constant value")
        self.btn_replace_nulls_value.setFixedSize(320, 40)
        #self.btn_replace_nulls_value.setEnabled(False)
        self.btn_replace_nulls_value.clicked.connect(self.funcs.replace_nulls_with_value)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_value, 1,1)
        
        # Añadir layouts individuales botones count null values y resto de botones
        self.layout_preprocesado.addLayout(layout_nulls_buttons)
        self.layout_preprocesado.setContentsMargins(0,20,0,0)       
        
        # Layout principal entrada y salida y preprocesado
        self.layout_entrada_salida_preprocesado = QHBoxLayout()
