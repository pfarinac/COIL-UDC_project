from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt


def model(x, y):
    clf = LinearRegression()
    clf.fit(x, y)
    prediccion = clf.predict(x)
    r2 = r2_score(y, prediccion)
    mse = mean_squared_error(y, prediccion)

    return clf, r2, mse


def graf(x, y, input_col: str, output_col: str, clf: LinearRegression):
    plt.scatter(x, y)
    plt.plot(x, clf.predict(x))
    plt.xlabel(input_col)
    plt.ylabel(output_col)
    plt.show()
