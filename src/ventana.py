from PyQt6.QtWidgets import  QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
from PyQt6.QtCore import QStandardPaths 
import sys


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
    
    #Añadir título, medidas, posición a la ventana y configurar el botón
    def inicializarUI(self):
        self.setGeometry(100,100,500,500)
        self.setWindowTitle("Ventana")

        #Crear layout vertical
        layout=QVBoxLayout()

        #Crear botón
        self.button = QPushButton("Añadir Archivo")
        self.button.clicked.connect(self.archivos)
        layout.addWidget(self.button)
        self.setLayout(layout)
    def archivos(self):

        #Se establece que el explorador de archivos se abrira en Descargas
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )
        #Tipos de archivos aceptados
        file_types = "CSV files (*.csv);;Excel files(*.xlsx);;Excel files(*.xls);;Sqlite files(*.sqlite);;DB files(*.db)"

        #Añadimos todas las configuraciones hechas
        self.file, _ =QFileDialog.getOpenFileName(self,"Open File",initial_dir, file_types)
if __name__=="__main__":
    app = QApplication(sys.argv)
    ventana=Ventana()
    ventana.show()
    sys.exit(app.exec()) # Al cerrar la aplicación se cierra la ventana