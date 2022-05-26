import pandas as pd


class DataFrameFormatter:
    
    def __init__(self, data_frame:pd.DataFrame):
        self.data_frame = data_frame

    def query_table(self, query_elem:str, query):
        """
        Queries the table using the parameters passed in 
        e.g, data_frame=correlation_input_df,query_elem='Period', query=2001. 
        Therefore correlation_input_df['Period]
        Args: 
            query_elem: the column in the table whose chosen value the table
                        will be filtered by.
            query: the value you want to filter the table with.
        """
        query_result = self.data_frame[self.data_frame[query_elem] == query]
        # make a copy of the slice of the dataframe that has the query
        query_result = query_result.copy()
        yield query_result

    def analysis_prep(self, analysis_table:pd.DataFrame, column_names:list):
        """
        Drop columns that you don't want in your analysis since they 
        probably don't aid it.
        Args:
            analysis_table: the data frame you want to drop columns from 
                        (usually on that has already been queried).
            column_names: the column names you want to drop from the column.

        """
        analysis_prepped_df = analysis_table.drop(column_names, axis=1)
        yield analysis_prepped_df

    def reshape_table(self, data_frame:pd.DataFrame, new_columns:str, new_index:str, new_values:str):
        """
        Reshapes the passed in dataframe/table to have a new index, new columns and new values.
        Args:
            data_frame: the dataframe you want to reshape.
            new_columns: the new columns you'd want when the dataframe has been reshaped
            new_index: the new index column you'd like the dataframe to have
            new_values: the new values you'd like the dataframe to have
        """
        reshaped_table = data_frame.pivot(index=new_index, columns=new_columns, values=new_values)
        yield reshaped_table



