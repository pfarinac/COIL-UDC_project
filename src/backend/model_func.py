from PyQt6.QtWidgets import (QLabel, QMessageBox)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


class MFuncs:
    """
    Clase que encapsula las funciones necesarias para gestionar un modelo de regresión lineal, 
    actualizar los datos, y mostrar gráficamente los resultados.
    """

    def __init__(self, data, figure: Figure, canvas: FigureCanvas, label_formula: QLabel, label_r2_mse: QLabel) -> None:
        """
        Inicializa una instancia de la clase MFuncs.

        Parámetros:
            data: Objeto que contiene los datos a procesar.
            figure (Figure): Figura de Matplotlib para la representación gráfica.
            canvas (FigureCanvas): Lienzo asociado a la figura para integrarla en la interfaz.
            label_formula (QLabel): Etiqueta para mostrar la fórmula del modelo.
            label_r2_mse (QLabel): Etiqueta para mostrar los valores de R^2 y MSE.
        """

        self.d_f = data
        self.figure = figure
        self.canvas = canvas
        self.label_formula = label_formula
        self.label_r2_mse = label_r2_mse

    def start_model(self):
        """
        Configura y entrena un modelo de regresión lineal utilizando los datos cargados.
        También genera una gráfica si se selecciona una sola columna de entrada.

        Muestra advertencias si los datos o las selecciones no son válidos.
        """
        self.update_input_output()
        self.update_df()

        self.model_input = self.input_col.copy()
        self.model_output = self.output_col
        if self.df is not None and self.input_col and self.output_col:

            self.model, self.r2, self.mse = self.create_model(
                self.df[self.model_input], self.df[self.model_output]
            )

            # Continuar con la lógica del modelo
            if len(self.model_input) == 1:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.scatter(self.df[self.model_input],
                           self.df[self.model_output], label='Data')
                ax.plot(self.df[self.model_input], self.model.predict(
                    self.df[self.model_input]), color='red', label='Adjustment')
                ax.set_xlabel(self.model_input[0])
                ax.set_ylabel(self.model_output)
                ax.set_title('Linear regression')
                ax.legend()
                self.canvas.setVisible(True)
            else:
                self.canvas.setVisible(False)
                QMessageBox.warning(
                    None, "Error", "You must select a single input column to be able to display the graph"
                )

            self.label_r2_mse.setVisible(True)
            self.label_formula.setText(
                self.formula(self.input_col, self.output_col))
            self.label_formula.setVisible(True)
            self.label_r2_mse.setText(f"R2= {self.r2} \nMSE= {self.mse}")
            self.canvas.draw()
        else:
            QMessageBox.warning(
                None, "Error", "The loaded data is incorrect, make sure you selected it correctly"
            )

    def formula(self, input_col, output_col):
        """
        Genera la fórmula del modelo lineal en formato texto.

        Parámetros:
            input_col (list): Lista de nombres de las columnas de entrada.
            output_col (str): Nombre de la columna de salida.

        Returns:
            str: Fórmula del modelo lineal.
        """
        formula = f"{output_col} = "
        for i in range(len(input_col)):
            formula += f"{input_col[i]}  *  {self.model.coef_[i]}  +  "
        formula += f" {self.model.intercept_}"
        return formula

    def update_input_output(self):
        """
        Actualiza las columnas de entrada y salida seleccionadas desde el objeto de datos.
        """
        self.input_col = self.d_f.input_col
        self.output_col = self.d_f.output_col

    def update_df(self):
        """
        Actualiza el DataFrame utilizado en base al objeto de datos proporcionado.
        """
        self.df = self.d_f.df

    def create_model(self, x, y):
        """
        Crea un modelo de regresión lineal con los datos proporcionados.

        Parámetros:
            x: DataFrame con las columnas de entrada.
            y: Serie con la columna de salida.

        Returns:
            LinearRegression: Modelo de regresión lineal.
            float: Coeficiente de determinación R^2 del modelo.
            float: Error cuadrático medio (MSE) del modelo.
        """
        clf = LinearRegression()
        clf.fit(x, y)
        prediccion = clf.predict(x)
        r2 = r2_score(y, prediccion)
        mse = mean_squared_error(y, prediccion)

        return clf, r2, mse
