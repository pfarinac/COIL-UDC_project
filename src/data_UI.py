from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, 
QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
QHeaderView, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget,QMainWindow,QInputDialog, QScrollArea, QTextEdit,QFrame)
from PyQt6.QtCore import QStandardPaths,Qt
from PyQt6.QtGui import QFont    
from data_func import *   
 # Titulo principal
class UI:
    def __init__(self) -> None:
        self.layout = QVBoxLayout()
        self.inicializar()
    def inicializar(self):
        self.viewer_title = QLabel("Data visualization")
        self.viewer_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.viewer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.features_list = QListWidget()
        self.features_list.setFixedSize(370, 90)
        self.features_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        self.target_combo = QListWidget()
        self.target_combo.setFixedSize(370, 90)
        self.target_combo.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.file_path_label = QLabel("File path: No file uploaded.")
        self.table_widget = QTableWidget()
        self.table_widget.setFixedSize(1490, 300)
        self.d_f = Funcs(self.target_combo, self.features_list, self.file_path_label, self.table_widget)
        # Layout botones open y load
        layout_open_load = QHBoxLayout()
        # Añadir boton open
        self.load_button = QPushButton("Open")
        self.load_button.setFixedSize(60, 44)
        layout_open_load.addWidget(self.load_button)
        self.load_button.clicked.connect(self.d_f.load_file) # Conectar el boton a la funcion
        # Añadir etiqueta para mostrar la ruta del archivo
        self.file_path_label = self.d_f.file_path_label
        self.file_path_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout_open_load.addWidget(self.file_path_label)  # Añadir la etiqueta al layout
        # Añadir botón de carga de modelo
        self.load_model_button = QPushButton("Load model")
        self.load_model_button.setFixedSize(120, 44)
        layout_open_load.addWidget(self.load_model_button)
        #self.load_model_button.clicked.connect(self.load_model)  # Conectar el botón a la función de carga
        

        
        # Layout entrada y salida
        self.layout_entrada_salida = QVBoxLayout()
        self.layout_entrada_salida.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Añadir etiqueta con el titulo
        self.entrada_salida_titulo = QLabel("Select input and output columns")
        self.entrada_salida_titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout_entrada_salida.addWidget(self.entrada_salida_titulo)
        layout_selectores = QHBoxLayout()
        
        # Layout entrada
        layout_entrada = QVBoxLayout()
        # Añadir etiqueta para el titulo
        self.features_label = QLabel("Select input columns (features):")
        self.features_label.setStyleSheet("font-size: 16px;")
        layout_entrada.addWidget(self.features_label)
        

        # Añadir etiqueta para la seleccion de columnas de entrada


        layout_entrada.addWidget(self.features_list)

        # Layout salida
        layout_salida = QVBoxLayout()
        # Añadir etiqueta para el titulo
        self.target_label = QLabel("Select output columns (target):")
        self.target_label.setStyleSheet("font-size: 16px;")
        layout_salida.addWidget(self.target_label)
        # Añadir etiqueta para la seleccion de columna de salida

        layout_salida.addWidget(self.target_combo)
        
        # Añadir layouts individuales de entrada y salida
        layout_selectores.addLayout(layout_entrada)
        layout_selectores.addLayout(layout_salida)
        self.layout_entrada_salida.addLayout(layout_selectores)

        self.layout_entrada_salida.setContentsMargins(0,20,0,0)
        




        self.confirm = QPushButton("Confirm selection")
        self.confirm.setFixedSize(145, 50)
        self.features_list.clicked.connect(self.d_f.registrar_input)
        self.confirm.clicked.connect(self.d_f.almacenar)
        self.layout_entrada_salida.addWidget(self.confirm)
        self.layout_entrada_salida.setContentsMargins(0,20,0,0)  

        self.layout.addWidget(self.viewer_title)
        self.layout.addLayout(layout_open_load)
        self.layout.addWidget(self.table_widget)