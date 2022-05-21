import pandas as pd
import numpy as np


class ColumnFormatter:

    def ___init__(self, column:pd.Series):
        self.column = column
        # convert colum to a list
        self.column_to_list = self.column.to_list()

    def enumerate_column(self):
        """Enumerates the items in the column"""
        enumerated = enumerate(np.unique(self.column_to_list))
        target_dict = {k: v for v, k in enumerated}
        return target_dict
    
    def replace_column_values(self, target_map):
        """
        Replaces the values in the column with their corresponding target dictionary value
        Args:
            target_map: target dictionary
        """
        for i in range(len(self.column_to_list)):
            self.column.replace(self.column_to_list[i], target_map[self.column_to_list[i]], inplace=True)

        print("Values replaced successfully")
