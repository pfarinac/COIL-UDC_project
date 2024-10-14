from cargar_datos import *
from PyQt6.QtWidgets import  QApplication
import sys 
from ventana import *

# Función principal
if __name__ == "__main__":
    #archivo = 'housing.xlsx'
    #cargar_datos(archivo)
    app = QApplication((sys.argv))
    ventana=Ventana()
    ventana.show()
    sys.exit(app.exec())
