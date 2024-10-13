import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Simple")
ventana.geometry("500x500")

# Función para mostrar un mensaje al presionar el botón
def mostrar_mensaje():
    messagebox.showinfo("Mensaje", "¡Has presionado el botón!")

# Crear el botón y asociarlo a la función 'mostrar_mensaje'
boton = tk.Button(ventana, text="Presionar", command=mostrar_mensaje)
boton.pack(pady=100)

# Crear un cuadro de texto para que el usuario ingrese datos
entrada_texto = tk.Entry(ventana)
entrada_texto.pack(pady=10)


ventana.mainloop()