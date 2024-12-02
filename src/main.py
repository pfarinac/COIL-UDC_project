from PyQt6.QtWidgets import  QApplication
import sys 
from frontend.ventana import *
from frontend.hoja_estilo import stylesheet

# Función principal
if __name__ == "__main__":
    app = QApplication((sys.argv))
    app.setStyleSheet(stylesheet)
    ventana=CsvViewer()
    ventana.show()
    sys.exit(app.exec())
