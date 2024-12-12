from PyQt6.QtWidgets import (QPushButton,
                             QVBoxLayout, QTableWidget, QLabel, QHBoxLayout, QListWidget, QHeaderView)
from PyQt6.QtCore import Qt
from backend.data_func import Funcs


class UI:
    """
    Clase que gestiona la interfaz de usuario para la visualización de datos, selección de columnas y botones de
    abrir archivos y carga de modelos.
    """

    def __init__(self) -> None:
        """
        Inicializa los componentes básicos de la interfaz de usuario.
        """
        self.layout = QVBoxLayout()
        self.inicializar()

    def inicializar(self):
        """
        Configura y organiza los elementos de la interfaz gráfica, incluyendo:
        - Títulos
        - Listas de selección para columnas de entrada y salida
        - Botones para abrir archivos y cargar modelos
        - Tabla para la visualización de datos
        """
        # Título de la interfaz
        self.viewer_title = QLabel("Data visualization")
        self.viewer_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.viewer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Lista de selección para las columnas de entrada
        self.features_list = QListWidget()
        self.features_list.setFixedSize(370, 90)
        self.features_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection)

        # Lista de selección para la columna objetivo
        self.target_combo = QListWidget()
        self.target_combo.setFixedSize(370, 90)
        self.target_combo.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_path_label = QLabel("File path: No file uploaded.")

        # Tabla para mostrar los datos cargados
        self.table_widget = QTableWidget()
        self.table_widget.setFixedSize(1490, 300)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        # Instancia de la clase Funcs para manejar datos y eventos
        self.d_f = Funcs(self.target_combo, self.features_list,
                         self.file_path_label, self.table_widget)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_path_label = self.d_f.file_path_label
        self.file_path_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;")

        # Configuración del layout para los botones "Open" y "Load model"
        layout_open_load = QHBoxLayout()

        # Botón para abrir archivos
        self.load_button = QPushButton("Open")
        self.load_button.setFixedSize(60, 44)
        layout_open_load.addWidget(self.load_button)
        self.load_button.clicked.connect(self.d_f.load_file)

       # Añadir etiqueta de ruta del archivo al layout
        layout_open_load.addWidget(self.file_path_label)

        # Botón de carga de modelo
        self.load_model_button = QPushButton("Load model")
        self.load_model_button.setFixedSize(120, 44)
        layout_open_load.addWidget(self.load_model_button)

        # Configuración del layout para la selección de entrada y salida
        self.layout_entrada_salida = QVBoxLayout()
        self.layout_entrada_salida.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Título del selector de columnas
        self.entrada_salida_titulo = QLabel("Select input and output columns")
        self.entrada_salida_titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold;")
        self.layout_entrada_salida.addWidget(self.entrada_salida_titulo)

        # Layout para las listas de entrada y salida
        layout_selectores = QHBoxLayout()

        # Configuración del layout entrada
        layout_entrada = QVBoxLayout()
        self.features_label = QLabel("Select input columns (features):")
        self.features_label.setStyleSheet("font-size: 16px;")
        layout_entrada.addWidget(self.features_label)
        layout_entrada.addWidget(self.features_list)

        # Configuración del layout salida
        layout_salida = QVBoxLayout()
        self.target_label = QLabel("Select output columns (target):")
        self.target_label.setStyleSheet("font-size: 16px;")
        layout_salida.addWidget(self.target_label)
        layout_salida.addWidget(self.target_combo)

        # Añadir los layouts de entrada y salida al layout general
        layout_selectores.addLayout(layout_entrada)
        layout_selectores.addLayout(layout_salida)
        self.layout_entrada_salida.addLayout(layout_selectores)
        self.layout_entrada_salida.setContentsMargins(0, 20, 0, 0)

        # Botón de confirmación de selección
        self.confirm = QPushButton("Confirm selection")
        self.confirm.setFixedSize(145, 50)
        self.features_list.clicked.connect(self.d_f.registrar_input)
        self.confirm.clicked.connect(self.d_f.almacenar)
        self.layout_entrada_salida.addWidget(self.confirm)
        self.layout_entrada_salida.setContentsMargins(0, 20, 0, 0)

        # Agregar elementos al layout principal
        self.layout.addWidget(self.viewer_title)
        self.layout.addLayout(layout_open_load)
        self.layout.addWidget(self.table_widget)
