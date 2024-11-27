stylesheet = """
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
    """