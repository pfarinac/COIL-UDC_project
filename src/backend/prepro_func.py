from PyQt6.QtWidgets import (QMessageBox, QInputDialog)


class PFuncs:
    """
    Clase para gestionar un preprocesado de datos trabajando con valores nulos,
    incluyendo su conteo, eliminación o reemplazo con diferentes métodos.
    """

    def __init__(self, data) -> None:
        """
        Inicializa una instancia de la clase PFuncs.

        Parámetros:
            data: Instancia de clase Funcs del archivo data_func
        """
        self.table_widget = None
        self.d_f = data

    def count_nulls(self):
        """
        Cuenta el número de valores nulos en las columnas seleccionadas del DataFrame.

        Muestra advertencias si no hay datos cargados.
        """
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        check_nulls = []  # Lista de prueba para comprobar si no hay ningun nulo
        self.no_nulls = False  # Indicador de que no hay nulos
        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
            for _, i in null_counts.items():
                if i == 0:
                    check_nulls.append(True)
            if len(check_nulls) == len(columns_to_process):
                self.no_nulls = True
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join(
                [f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(
                None, "Null values", f"Number of null values ​​per column:\n{null_info}")

        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def remove_nulls(self):
        """
        Elimina las filas que contienen valores nulos en las columnas seleccionadas del DataFrame
        y actualiza la tabla en la interfaz.

        Muestra advertencias si no hay datos cargados.
        """
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]
            original_shape = self.df.shape
            self.df.dropna(subset=columns_to_process, inplace=True)
            self.d_f.update_table(self.table_widget, self.df)
            QMessageBox.information(
                None, "Deleted Rows", f" {original_shape[0] - self.df.shape[0]} rows with null values in the selectd columns were deleted.")

        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def replace_nulls_with_mean(self):
        """
        Reemplaza los valores nulos en las columnas seleccionadas con la media de cada columna
        y actualiza la tabla en la interfaz.

        Muestra advertencias si no hay datos cargados.
        """
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]

            for col in columns_to_process:
                if self.df[col].isnull().any():
                    mean_value = self.df[col].mean()
                    self.df[col].fillna(mean_value, inplace=True)
            self.d_f.update_table(self.table_widget, self.df)
            QMessageBox.information(
                None, "Replaced values", "Null values ​​have been replaced by the mean of the selected columns.")

        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def replace_nulls_with_median(self):
        """
        Reemplaza los valores nulos en las columnas seleccionadas con la mediana de cada columna
        y actualiza la tabla en la interfaz.

        Muestra advertencias si no hay datos cargados.
        """
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        if self.df is not None:
            columns_to_process = self.input_col + [self.output_col]

            for col in columns_to_process:
                if self.df[col].isnull().any():
                    median_value = self.df[col].median()
                    self.df[col].fillna(median_value, inplace=True)
            self.d_f.update_table(self.table_widget, self.df)
            QMessageBox.information(
                None, "Replaced values", "Null values ​​have been replaced by the median of the selected columns.")

        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def replace_nulls_with_value(self):
        """
        Solicita al usuario un valor constante para reemplazar los valores nulos en las columnas seleccionadas
        y actualiza la tabla en la interfaz.

        Muestra advertencias si no hay datos cargados o si el usuario no proporciona un valor válido.
        """
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        print(self.input_col)
        if self.df is not None:
            value, ok = QInputDialog.getText(
                None, "Replace nulls with constant value", "Enter the value to replace nulls:")
            if ok and value:
                columns_to_process = self.input_col + [self.output_col]

                for col in columns_to_process:
                    if self.df[col].isnull().any():
                        self.df[col].fillna(value, inplace=True)
                self.d_f.update_table(self.table_widget, self.df)
                QMessageBox.information(
                    None, "Replaced values", f"Null values has been replaced by '{value}' in the selected columns.")

            else:
                QMessageBox.warning(
                    None, "Warning", "Please enter a valid value to replace nulls.")
        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def update_df(self):
        """
        Actualiza el DataFrame utilizado.
        """
        self.df = self.d_f.df

    def update_wtable(self):
        """
        Actualiza el widget de tabla utilizado en la interfaz.
        """
        self.table_widget = self.d_f.table_widget

    def update_input_output(self):
        """
        Actualiza las columnas de entrada y salida seleccionadas desde el objeto de datos.
        """
        self.input_col = self.d_f.input_col
        self.output_col = self.d_f.output_col
