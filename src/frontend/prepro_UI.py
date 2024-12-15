from PyQt6.QtWidgets import (QPushButton,
                             QVBoxLayout, QLabel, QGridLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
from backend.prepro_func import PFuncs


class PUI:
    """
    Clase que administra la interfaz gráfica para realizar preprocesamiento
    de datos, incluyendo el manejo de valores nulos mediante diversas opciones.

    Atributos:
        layout (QVBoxLayout): Layout principal de la interfaz.
        d_f: Datos utilizados para inicializar las funcionalidades del preprocesamiento.
        funcs (PFuncs): Clase de backend que administra las funciones de preprocesamiento.
    """
    def __init__(self, data) -> None:
        """
        Inicializa una instancia de la clase PUI.

        Parámetros:
            data: Instancia de clase Funcs del archivo data_func
        """
        self.layout = QVBoxLayout
        self.d_f = data
        self.funcs = PFuncs(self.d_f)
        self.inicializar()

    def inicializar(self):
        """
        Configura la interfaz gráfica inicial, incluyendo:
        - Botón para contar valores nulos.
        - Botones para diferentes opciones de manejo de valores nulos.
        - Layouts organizados para facilitar la interacción del usuario.
        """

        # Layout secundario preprocesado
        self.layout_preprocesado = QVBoxLayout()
        self.layout_preprocesado.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout_preprocesado.setContentsMargins(5, 20, 0, 0)

        # Layout para el botón "Count null values"
        layout_count_nulls = QGridLayout()

        # Etiqueta de título del preprocesamiento
        self.prep_title = QLabel("Data preprocessing")
        self.prep_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout_preprocesado.addWidget(self.prep_title)

        layout_count_nulls.setContentsMargins(0, 7, 0, 0)
        self.layout_preprocesado.addLayout(layout_count_nulls)

        # Botón "Count null values"
        self.btn_count_nulls = QPushButton("Count null values")
        self.btn_count_nulls.setFixedSize(645, 40)
        self.btn_count_nulls.setEnabled(False)
        self.btn_count_nulls.clicked.connect(self.funcs.count_nulls)
        self.btn_count_nulls.clicked.connect(
            self.habilitar_botones_preprocesado)
        layout_count_nulls.addWidget(self.btn_count_nulls)

        # Layout para los botones de manejo de valores nulos

        layout_nulls_buttons = QGridLayout()

        # Botón para eliminar filas con nulos
        self.btn_remove_nulls = QPushButton("Delete rows with nulls")
        self.btn_remove_nulls.setFixedSize(320, 40)
        self.btn_remove_nulls.setEnabled(False)
        self.btn_remove_nulls.clicked.connect(self.funcs.remove_nulls)
        layout_nulls_buttons.addWidget(self.btn_remove_nulls, 0, 0)
        
        # Botón para reemplazar nulos por la media
        self.btn_replace_nulls_mean = QPushButton("Replace nulls with mean")
        self.btn_replace_nulls_mean.setFixedSize(320, 40)
        self.btn_replace_nulls_mean.setEnabled(False)
        self.btn_replace_nulls_mean.clicked.connect(
            self.funcs.replace_nulls_with_mean)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_mean, 0, 1)
        
        # Botón para reemplazar nulos por la mediana
        self.btn_replace_nulls_median = QPushButton(
            "Replace nulls with median")
        self.btn_replace_nulls_median.setFixedSize(320, 40)
        self.btn_replace_nulls_median.setEnabled(False)
        self.btn_replace_nulls_median.clicked.connect(
            self.funcs.replace_nulls_with_median)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_median, 1, 0)
        
        # Botón para reemplazar nulos por un valor constante
        self.btn_replace_nulls_value = QPushButton(
            "Replace nulls with constant value")
        self.btn_replace_nulls_value.setFixedSize(320, 40)
        self.btn_replace_nulls_value.setEnabled(False)
        self.btn_replace_nulls_value.clicked.connect(
            self.funcs.replace_nulls_with_value)
        layout_nulls_buttons.addWidget(self.btn_replace_nulls_value, 1, 1)

        # Añadir los layouts de botones al layout principal de preprocesamiento
        self.layout_preprocesado.addLayout(layout_nulls_buttons)
        self.layout_preprocesado.setContentsMargins(0, 20, 0, 0)

        # Layout principal entrada y salida y preprocesado
        self.layout_entrada_salida_preprocesado = QHBoxLayout()

    def habilitar_botones_preprocesado(self):
        """
        Habilita o deshabilita los botones de manejo de valores nulos según el estado de los datos.

        Si no hay valores nulos, los botones permanecerán deshabilitados.
        """
        if self.funcs.no_nulls == False:
            self.btn_remove_nulls.setEnabled(True)
            self.btn_replace_nulls_mean.setEnabled(True)
            self.btn_replace_nulls_median.setEnabled(True)
            self.btn_replace_nulls_value.setEnabled(True)
        else:
            self.btn_remove_nulls.setEnabled(False)
            self.btn_replace_nulls_mean.setEnabled(False)
            self.btn_replace_nulls_median.setEnabled(False)
            self.btn_replace_nulls_value.setEnabled(False)
