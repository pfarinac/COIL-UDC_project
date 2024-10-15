import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit

# Crear la clase de la ventana principal
class VentanaSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Establecer el título de la ventana
        self.setWindowTitle('Ventana Simple con PyQt6')

        # Tamaño de la ventana
        self.setGeometry(100,100,250,250)
        # Crear un layout vertical
        layout = QVBoxLayout()

        # Crear un cuadro de texto donde el usuario puede ingresar datos
        self.entrada_texto = QLineEdit(self)
        self.entrada_texto.setPlaceholderText('Escribe algo aquí...')
        layout.addWidget(self.entrada_texto)

        # Crear un botón y conectarlo a una función para mostrar un mensaje
        boton = QPushButton('Presionar', self)
        boton.clicked.connect(self.mostrar_mensaje)
        layout.addWidget(boton)

        # Establecer el layout para la ventana
        self.setLayout(layout)

    def mostrar_mensaje(self):
        # Obtener el texto ingresado en el cuadro de texto
        texto_ingresado = self.entrada_texto.text()

        # Mostrar un mensaje con el texto ingresado
        QMessageBox.information(self, 'Mensaje', f'Has presionado el botón. Texto ingresado: {texto_ingresado}')

# Crear la aplicación y la ventana principal
app = QApplication(sys.argv)
ventana = VentanaSimple()
ventana.show()

# Ejecutar el bucle principal de la aplicación
sys.exit(app.exec())