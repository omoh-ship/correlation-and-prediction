import pandas as pd


class ColumnFormatter:

    def ___init__(self, column:pd.Series):
        self.column = column
        # convert colum to a list
        self.column_to_list = self.column.to_list()

    def enumerate_column(self):
        