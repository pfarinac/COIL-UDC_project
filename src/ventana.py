from PyQt6.QtWidgets import (QApplication, QWidget,
                             QVBoxLayout, QMainWindow, QScrollArea)
from PyQt6.QtCore import Qt
import sys
from modelo_lineal import model
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from data_func import *
from data_UI import *
from prepro_UI import *
from model_UI import *
from SLD_UI import *


class CsvViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado

        self.inicializarUI()

    def inicializarUI(self):

        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1920, 1080)

        self.d_u = UI()
        self.p_u = PUI(self.d_u.d_f)
        self.m_u = MUI(self.d_u.d_f)
        self.sld_u = SLDUI(self.m_u.funcs)
        self.d_u.confirm.clicked.connect(self.habilitar_count_nulls)
        self.p_u.btn_count_nulls.clicked.connect(self.habilitar_model_button)

        self.m_u.model_button.clicked.connect(self.deshabilitar_buttons)
        self.m_u.model_button.clicked.connect(
            self.sld_u.funcs.reset_input_fields)
        self.m_u.model_button.clicked.connect(self.enable_model)

        self.d_u.load_model_button.clicked.connect(self.sld_u.funcs.load_model)
        self.d_u.load_model_button.clicked.connect(self.display_loaded_model)
        self.d_u.load_model_button.clicked.connect(
            self.sld_u.enable_prediction)

        self.p_u.layout_entrada_salida_preprocesado.addLayout(
            self.d_u.layout_entrada_salida)
        self.p_u.layout_entrada_salida_preprocesado.addLayout(
            self.p_u.layout_preprocesado)
        self.p_u.layout_entrada_salida_preprocesado.setAlignment(
            Qt.AlignmentFlag.AlignCenter)

        self.m_u.layout_visualizar_iniciar_modelo.addLayout(
            self.sld_u.layout_descripcion_modelo)

        # Creamos el layout principal y le añadimos los auxiliares
        layout = QVBoxLayout()
        layout.addLayout(self.d_u.layout)
        layout.addLayout(self.p_u.layout_entrada_salida_preprocesado)
        layout.addLayout(self.m_u.layout_visualizar_iniciar_modelo)
        layout.addLayout(self.sld_u.layout_mostrar_prediccion)
        layout.addLayout(self.sld_u.layout_guardarmodelo_prediccion)

        container = QWidget()
        container.setLayout(layout)

        # Crear un área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Desactiva el scroll horizontal
        # Activa el scroll vertical solo si es necesario
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Crear el diseño principal y añadir el área de scroll
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(scroll_area)

        # Configurar el diseño principal para la ventana
        self.setCentralWidget(main_widget)

    def habilitar_count_nulls(self):
        self.p_u.btn_count_nulls.setEnabled(True)

    def habilitar_model_button(self):
        self.m_u.model_button.setEnabled(True)

    def deshabilitar_buttons(self):
        self.p_u.btn_count_nulls.setEnabled(False)
        self.p_u.btn_remove_nulls.setEnabled(False)
        self.p_u.btn_replace_nulls_mean.setEnabled(False)
        self.p_u.btn_replace_nulls_median.setEnabled(False)
        self.p_u.btn_replace_nulls_value.setEnabled(False)
        self.m_u.model_button.setEnabled(False)

    def display_loaded_model(self, model_data):
        # Ocultar secciones de carga de datos y selección de columnas
        self.d_u.table_widget.hide()
        self.d_u.features_label.hide()
        self.d_u.features_list.hide()
        self.d_u.target_label.hide()
        self.d_u.target_combo.hide()
        self.d_u.viewer_title.hide()
        self.p_u.prep_title.hide()
        self.m_u.model_title.hide()
        self.d_u.entrada_salida_titulo.hide()
        # Botones de preprocesado
        self.p_u.btn_count_nulls.hide()
        self.p_u.btn_remove_nulls.hide()
        self.p_u.btn_replace_nulls_mean.hide()
        self.p_u.btn_replace_nulls_median.hide()
        self.p_u.btn_replace_nulls_value.hide()
        self.d_u.confirm.hide()
        self.m_u.model_button.hide()
        self.d_u.load_button.hide()
        self.d_u.file_path_label.hide()
        self.sld_u.save_button.setEnabled(True)
        # Modelo
        self.m_u.canvas.hide()
        self.m_u.graph_widget.hide()
        self.m_u.label_formula.setVisible(True)
        self.m_u.label_r2_mse.setVisible(True)
        self.sld_u.result_label.setVisible(False)

        # Mostrar los detalles del modelo cargado
        if "model" in self.sld_u.funcs.loaded_model_data:
            # Actualizar etiquetas
            self.m_u.label_formula.setText(
                f"Model formula: {self.m_u.funcs.formula(self.sld_u.funcs.model_input,self.sld_u.funcs.model_output)}")
            self.m_u.label_r2_mse.setText(
                f"R²: {self.sld_u.funcs.r2_score}  |  MSE: {self.sld_u.funcs.mse}")
            self.sld_u.description_text.setText(self.sld_u.funcs.description)

    def enable_model(self):
        self.sld_u.save_button.setEnabled(True)
        self.sld_u.predict_button.setEnabled(True)
        self.sld_u.enable_prediction()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QMainWindow {
        background-color: #000000;  /* Fondo negro */
    }
    QWidget {
        background-color: #000000;  /* Fondo negro para widget principal */
    }
    QLabel {
        color: #FFFFFF;            /* Título en blanco */
        font-size: 20px;
        font-weight: bold;
    }
    QLineEdit, QTextEdit {
        background-color: #1E1E1E; /* Gris oscuro para entrada */
        color: #FFFFFF;            /* Texto blanco */
        border: 1px solid #444444; /* Borde gris oscuro */
        padding: 5px;
        font-size: 14px;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #00C853; /* Verde vibrante al enfocar */
    }
    QTableWidget {
        background-color: #1E1E1E; /* Gris oscuro para fondo de tabla */
        color: #FFFFFF;            /* Texto blanco */
        border: 2px solid #00C853; /* Borde verde vibrante */
        gridline-color: #444444;   /* Líneas de cuadrícula grises */
    }
    QHeaderView::section {
        background-color: #2E2E2E; /* Gris oscuro para encabezados */
        color: #FFFFFF;            /* Texto blanco en encabezados */
        font-weight: bold;
        border: 1px solid #444444; /* Borde gris oscuro */
        padding: 4px;
    }
    QPushButton {
        background-color: #00C853; /* Verde vibrante */
        color: #FFFFFF;            /* Texto blanco */
        border: 1px solid #00E676; /* Borde verde más claro */
        padding: 12px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #00E676; /* Verde más claro al pasar el ratón */
    }
    QPushButton:pressed {
        background-color: #00BFA5; /* Verde intenso al presionar */
    }
    QPushButton:disabled {
        background-color: #555555; /* Gris oscuro para botones desactivados */
        color: #AAAAAA;            /* Texto gris claro para botones desactivados */
        border: 1px solid #444444; /* Borde gris más oscuro */
    }
    QListWidget {
        background-color: #2E2E2E; /* Gris oscuro para fondo */
        color: #FFFFFF;            /* Texto blanco */
        border: 2px solid #00C853; /* Borde verde vibrante */
        padding: 5px;
    }
    QListWidget::item {
        color: #FFFFFF;            /* Texto blanco */
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #00C853; /* Verde para elemento seleccionado */
        color: #000000;            /* Texto negro en selección */
    }
    QScrollBar:vertical {
        background: #1E1E1E;       /* Fondo oscuro */
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: #00C853;       /* Verde para el scroll */
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;          /* Sin flechas */
    }
    """)
    viewer = CsvViewer()
    viewer.show()
    sys.exit(app.exec())
