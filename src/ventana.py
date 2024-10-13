from PyQt6.QtWidgets import  QApplication, QWidget 
import sys

#boton=QPushButton("Abrir archivo")
class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
    #Añadimos título, medidas y posición a la ventana
    def inicializarUI(self):
        self.setGeometry(100,100,500,500)
        self.setWindowTitle("Ventana")
        self.show()
if __name__=="__main__":
    app = QApplication(sys.argv)
    ventana=Ventana()
    sys.exit(app.exec()) # Al cerrar la aplicación se cierra la ventana