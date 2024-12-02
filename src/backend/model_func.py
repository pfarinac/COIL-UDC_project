from PyQt6.QtWidgets import (QLabel, QMessageBox)
from backend.modelo_lineal import model
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from backend.modelo_lineal import model


class MFuncs:
    def __init__(self, data, figure: Figure, canvas: FigureCanvas, label_formula: QLabel, label_r2_mse: QLabel) -> None:
        self.d_f = data
        self.figure = figure
        self.canvas = canvas
        self.label_formula = label_formula
        self.label_r2_mse = label_r2_mse
    # Método para crear el modelo y mostrar la gráfica

    def start_model(self):
        self.update_input_output()
        self.update_df()
        # Limpiar campos de entrada anteriores antes de iniciar un nuevo modelo
        self.model_input = self.input_col.copy()
        self.model_output = self.output_col
        if self.df is not None and self.model_input and self.model_output:
            self.model, self.r2, self.mse = model(
                self.df[self.model_input], self.df[self.model_output])
            if len(self.model_input) == 1:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.scatter(self.df[self.model_input],
                           self.df[self.model_output], label='Data')
                ax.plot(self.df[self.model_input], self.model.predict(
                    self.df[self.model_input]), color='red', label='Adjustment')
                ax.set_xlabel(self.model_input[0])
                ax.set_ylabel(self.model_output)
                ax.set_title('Lineal regression')
                ax.legend()
                self.canvas.setVisible(True)
            else:
                self.canvas.setVisible(False)
                QMessageBox.warning(
                    None, "Error", "You must select a single input column to be able to display the graph")

            self.label_r2_mse.setVisible(True)
            self.label_formula.setText(self.formula(self.input_col,self.output_col))
            self.label_formula.setVisible(True)
            self.label_r2_mse.setText(f"R2= {self.r2} \nMSE= {self.mse}")
            self.canvas.draw()

    def formula(self, input_col, output_col):
        formula = f"{output_col} = "
        for i in range(len(input_col)):
            formula += f"{input_col[i]}  *  {self.model.coef_[i]}  +  "
        formula += f" {self.model.intercept_}"
        return formula

    def update_input_output(self):
        self.input_col = self.d_f.input_col
        self.output_col = self.d_f.output_col

    def update_df(self):
        self.df = self.d_f.df
