from PyQt6.QtWidgets import (QLabel, QMessageBox)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


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
        # Limpiar campos de entrada anteriores
        self.model_input = self.input_col.copy()
        self.model_output = self.output_col
        if self.df is not None and self.input_col and self.output_col:
            # Intentar generar el modelo solo si las condiciones se cumplen
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
            self.label_formula.setText(self.formula(self.input_col,self.output_col))
            self.label_formula.setVisible(True)
            self.label_r2_mse.setText(f"R2= {self.r2} \nMSE= {self.mse}")
            self.canvas.draw()
        else:
            QMessageBox.warning(
                    None, "Error", "The loaded data is incorrect, make sure you selected it correctly"
                )



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

    def create_model(self,x, y):
        clf = LinearRegression()
        clf.fit(x, y)
        prediccion = clf.predict(x)
        r2 = r2_score(y, prediccion)
        mse = mean_squared_error(y, prediccion)

        return clf, r2, mse
