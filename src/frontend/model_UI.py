from PyQt6.QtWidgets import (QWidget, QPushButton,
                             QVBoxLayout, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from backend.model_func import MFuncs


class MUI:
    """
    Clase que administra la interfaz de usuario para visualizar gráficos y
    fórmulas, manejando el inicio del modelo utilizando datos y funcionalidades del backend.

    Atributos:
        layout (QVBoxLayout): Layout principal de la interfaz.
        d_f: Instacia de Funcs de data_funcs
        figure (Figure): Objeto de matplotlib para generar gráficos.
        canvas (FigureCanvas): Lienzo para mostrar los gráficos en la interfaz.
        label_formula (QLabel): Etiqueta para mostrar la fórmula del modelo.
        label_r2_mse (QLabel): Etiqueta para mostrar valores de R² y MSE.
        funcs (MFuncs): Clase de backend que administra las funcionalidades del modelo.
    """

    def __init__(self, data) -> None:
        """
        Inicializa una instancia de la clase MUI.

        Parámetros:
            data: Datos utilizados para inicializar las funcionalidades del modelo.
        """
        self.layout = QVBoxLayout()
        self.d_f = data
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.label_formula = QLabel("")
        self.label_r2_mse = QLabel("")
        self.funcs = MFuncs(self.d_f, self.figure, self.canvas,
                            self.label_formula, self.label_r2_mse)
        self.inicializar()

    def inicializar(self):
        """
        Configura la interfaz gráfica inicial, incluyendo layouts para:
        - Gráficos y fórmulas
        - Botones y acciones del modelo
        """

        # Layout para gráfica y fórmula
        layout_graph_formula = QHBoxLayout()

        # Configuración del widget para el gráfico
        self.graph_widget = QWidget()  # Usamos QWidget en lugar de QGroupBox
        self.graph_widget.setStyleSheet("""
            QWidget {
                font-size: 16px;
                font-weight: bold;
                color: white; /* Texto en blanco */
                background-color: #1E1E1E; /* Fondo gris oscuro */
                border: 2px solid #00C853; /* Borde verde vibrante */
                border-radius: 5px; /* Esquinas redondeadas */
                padding: 10px; /* Espaciado interno */
            }
        """)

        # Layout interno para la gráfica
        self.graph_layout = QVBoxLayout()
        self.graph_widget.setLayout(self.graph_layout)

        # Configuración del título y el canvas del gráfico
        self.graph_title = QLabel("Graph")
        self.graph_title.setStyleSheet(
            "font-weight: bold; font-size: 16px; color: white; background: transparent; border: none;")
        self.canvas.setFixedSize(700, 400)
        self.canvas.setVisible(False)

        # Agregar widgets al layout de la gráfica
        self.graph_layout.addWidget(self.graph_title)
        self.graph_layout.addWidget(self.canvas)

        # Layout para la fórmula
        self.formula_layout = QVBoxLayout()

        # Configuración del título y etiquetas de la fórmula
        self.formula_title = QLabel("Formula")
        self.formula_title.setStyleSheet(
            "font-weight: bold; font-size: 16px; color: white;")
        
        self.label_formula.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: white;")
        self.label_formula.setVisible(False)

        self.label_r2_mse.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: white;")
        self.label_r2_mse.setVisible(False)

        # Se agregan widgets al layout de la fórmula
        self.formula_layout.addWidget(self.formula_title)
        self.formula_layout.addWidget(self.label_formula)
        self.formula_layout.addWidget(self.label_r2_mse)

        # Contenedor del layout de la fórmula
        self.formula_widget = QWidget()
        self.formula_widget.setLayout(self.formula_layout)

        # Estilos solo para el contenedor del widget
        self.formula_widget.setStyleSheet("""QWidget {
            background-color: #1E1E1E;  /* Gris oscuro para fondo */
            border: 2px solid #00C853;  /* Borde verde vibrante */
            border-radius: 5px;         /* Esquinas redondeadas */
            padding: 10px;              /* Espaciado interno */
            }
            QLabel {border: 0px}
        """)

        # Agregar widgets de gráfico y fórmula al layout principal
        layout_graph_formula.addWidget(self.graph_widget)
        layout_graph_formula.addWidget(self.formula_widget)

        # Layout visualizar y gestionar modelo
        self.layout_visualizar_iniciar_modelo = QVBoxLayout()
        self.model_title = QLabel("View and start model")
        self.model_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout_visualizar_iniciar_modelo.addWidget(self.model_title)
        
        # Configuración del botón para iniciar el modelo   
        layout_boton_start = QGridLayout()
        self.model_button = QPushButton("Start model")
        self.model_button.setFixedSize(135, 40)
        self.model_button.setEnabled(False)
        self.model_button.clicked.connect(self.funcs.start_model)
        layout_boton_start.addWidget(self.model_button)
        layout_boton_start.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Agregar layouts al contenedor principal
        self.layout_visualizar_iniciar_modelo.addLayout(layout_boton_start)
        self.layout_visualizar_iniciar_modelo.addLayout(layout_graph_formula)
        self.layout_visualizar_iniciar_modelo.setContentsMargins(0, 20, 0, 20)
