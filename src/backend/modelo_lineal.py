from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt





def graf(x, y, input_col: str, output_col: str, clf: LinearRegression):
    plt.scatter(x, y)
    plt.plot(x, clf.predict(x))
    plt.xlabel(input_col)
    plt.ylabel(output_col)
    plt.show()
