from PyQt6.QtWidgets import (QMessageBox, QInputDialog)


class PFuncs:
    def __init__(self, data) -> None:
        self.table_widget = None
        self.d_f = data

    def count_nulls(self):
        self.update_df()
        self.update_input_output()
        self.update_wtable()
        if self.df is not None:
            # Seleccionar solo las columnas de entrada y salida
            columns_to_process = self.input_col + [self.output_col]
            # Contar los valores nulos solo en las columnas seleccionadas
            null_counts = self.df[columns_to_process].isnull().sum()
            # Crear el mensaje con el conteo de valores nulos por cada columna
            null_info = "\n".join(
                [f"{col}: {count}" for col, count in null_counts.items()])
            QMessageBox.information(
                None, "Null values", f"Number of null values ​​per column:\n{null_info}")

        else:
            QMessageBox.warning(
                None, "Warning", "You must first upload a CSV, XLSX or SQLite file.")

    def remove_nulls(self):
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
        self.df = self.d_f.df

    def update_wtable(self):
        self.table_widget = self.d_f.table_widget

    def update_input_output(self):
        self.input_col = self.d_f.input_col
        self.output_col = self.d_f.output_col
