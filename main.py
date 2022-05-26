import pandas as pd
from column_formatter import ColumnFormatter

xls = pd.ExcelFile("sample_data.xlsx")

correlation_input_df = pd.read_excel(xls, 'Correlation Input Sheet')


def table_query(data_frame:pd.DataFrame, query_elem, query):
    """
    Queries the table using the parameters passed in e.g, data_frame=correlation_input_df,query_elem='Period', query=2001. Therefore correlation_input_df['Period]
    """
    query_result = data_frame[data_frame[query_elem] == query]
    # make a copy of the slice of the dataframe that has the query
    query_result = query_result.copy()
    yield query_result


def analysis_prep(data_frame:pd.DataFrame, column_names:list):
    """Drop columns that you don't want in your analysis since they probably don't aid it"""
    analysis_prepped_df = data_frame.drop(column_names, axis=1)
    yield analysis_prepped_df


def reshape_table(data_frame:pd.DataFrame, new_columns:str, new_index:str, new_values:str):
    reshaped_table = data_frame.pivot(index=new_index, columns=new_columns, values=new_values)
    yield reshaped_table


def correlation_operations(data_frame:pd.DataFrame, query_elem:str, query, 
                            columns_to_drop:list, new_index_column:str, new_columns:str, new_values:str):
    """
    Args:
        data_frame: data frame to be worked on
        query_elem: name of the column in the dataframe that you'll use to filter the dataframe
        query: the value you'll use to query the data frame
        columns_to_drop: columns you want ropped from the table as they don't ai analysis
        new_index_column: desired new index column when the table is reshaped
        new_columns: desired new columns when the table is reshaped
        new_vales: desired new index column when the table is reshaped
    """
    # Query table
    filter_table = table_query(data_frame=data_frame, query_elem=query_elem, query=query)
    result = [item for item in filter_table]
    result = pd.concat(result)
    print(f"Table successfully filtered with query:{result}\n\n")

    # drop useless columns
    refined_df = analysis_prep(data_frame=result, column_names=columns_to_drop)
    refined_result = [item for item in refined_df]
    refined_df = pd.concat(refined_result)
    print(f"Table successfully dropped columns not needed\n{refined_df}\n\n")

    #enumerate items in the desired new index column
    column_formatter = ColumnFormatter(refined_df[new_index_column])
    target_map = column_formatter.enumerate_column()
    print(f"New index column successfully enumerated\n\n")

    # replace current values in the column with their maped enumerated equivalent(it prints a confirmation message if successful)
    column_formatter.replace_column_values(target_map=target_map)

    # reshape the table
    reshaped_table = reshape_table(data_frame=refined_df, new_columns=new_columns, new_index=new_index_column, new_values=new_values)
    result = [item for item in reshaped_table]
    reshaped_table = pd.concat(result)

    # fill NaN values with 0
    reshaped_table = reshaped_table.fillna(0)

    reshaped_corr = reshaped_table.corr()
    print(reshaped_corr)


correlation_operations(data_frame=correlation_input_df, 
                        query_elem='Period',
                        query=2001,
                        columns_to_drop=['Source', 'Period', 'LGA'],
                        new_index_column='State',
                        new_columns='Indicator',
                        new_values='Value')

