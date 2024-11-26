from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# Definir la clase de la aplicación principal


class VentanaSimpleApp(App):
    def build(self):
        # Crear un BoxLayout vertical para organizar los elementos
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Crear un cuadro de texto para ingresar datos
        self.entrada_texto = TextInput(hint_text='Escribe algo aquí...')
        layout.add_widget(self.entrada_texto)

        # Crear un botón que muestra un mensaje al ser presionado
        boton = Button(text='Presionar', size_hint=(1, 0.2))
        boton.bind(on_press=self.mostrar_mensaje)
        layout.add_widget(boton)

        return layout

    def mostrar_mensaje(self, instance):
        # Obtener el texto ingresado
        texto_ingresado = self.entrada_texto.text

        # Crear un Popup para mostrar el mensaje
        popup = Popup(title='Mensaje',
                      content=Label(
                          text=f'Texto ingresado: {texto_ingresado}'),
                      size_hint=(0.8, 0.4))
        popup.open()


if __name__ == '__main__':
    VentanaSimpleApp().run()
