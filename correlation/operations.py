import pandas as pd
from data_frame_formatter import DataFrameFormatter
from column_formatter import ColumnFormatter

# xls = pd.ExcelFile("data/msdat_data.xlsx")

correlation_input_df = pd.read_excel('data/msdat_data.xlsx')


def prep_data(query_element: str, query_value, columns_to_drop: list,
              source_query: list, source: str,
              df_formatter):
    """
    Args:
        query_element: name of the column in the dataframe that you'll use
        to filter the dataframe.
        query_value: the value you'll use to query the data frame
        columns_to_drop: columns you want dropped from the table as they
        don't aid analysis.
        source_query: the list of sources you want to query for
        source: the column you want to query for sources.
        df_formatter: data_frame formatter object
    """

    # Filter table by source
    source_filter = df_formatter.filter_with_list(query_elem=source, query=source_query)
    result = [item for item in source_filter]
    result = pd.concat(result)
    # make provisions for if the df is empty
    # print(f"Table successfully filtered with query:{result}\n\n")

    # Query table by period
    filter_table = df_formatter.query_table(query_elem=query_element, query=query_value,
                                            data_frame=result)
    result = [item for item in filter_table]
    result = pd.concat(result)
    # print(f"Table successfully filtered with query:{result}\n\n")

    # drop useless columns
    refined_df = df_formatter.analysis_prep(analysis_table=result, column_names=columns_to_drop)
    refined_result = [item for item in refined_df]
    refined_df = pd.concat(refined_result)
    # print(f"Table successfully dropped columns not needed\n{refined_df}\n\n")

    yield refined_df


def correlation_operations(query_elem: str,
                           query_value, columns_to_drop: list,
                           source_query: list, source: str,
                           values_to_see: list, new_values: str,
                           new_index_column: str, new_columns: str,
                           correlation_input_df_formatter):
    """
    This function will works perfectly with the correlation input sheet
    but hasn't been abstracted to work with the other sheets yet.
    Args:
        query_elem: name of the column in the dataframe that you'll use
        to filter the dataframe.
        query_value: the value you'll use to query the data frame
        columns_to_drop: columns you want dropped from the table as they
        don't aid analysis.
        source_query: the list of sources you want to query for
        source: the column you want to query for sources.
        new_index_column: desired new index column when the table is reshaped
        new_columns: desired new columns when the table is reshaped
        new_values: desired new index column when the table is reshaped
        values_to_see: values in new_column you want to filter the table with
        correlation_input_df_formatter: data_frame_formatter object
    """

    refined_df = prep_data(query_element=query_elem,
                           df_formatter=correlation_input_df_formatter,
                           query_value=query_value, columns_to_drop=columns_to_drop,
                           source_query=source_query, source=source)

    refined_result = [item for item in refined_df]
    refined_df = pd.concat(refined_result)
    # filter table for the indicators you want to see on the heatmap
    new_indicator_table = refined_df[refined_df[new_columns].isin(values_to_see)]
    # print(new_indicator_table)

    # enumerate items in the desired new index column
    column_formatter = ColumnFormatter(new_indicator_table[new_index_column])
    target_map = column_formatter.enumerate_column()
    # print(f"New index column successfully enumerated\n\n")

    # replace current values in the column with their mapped enumerated equivalent
    # (it prints a confirmation message if successful)
    column_formatter.replace_column_values(target_map=target_map)

    # reshape the table
    reshaped_table = correlation_input_df_formatter.reshape_table(data_frame=new_indicator_table,
                                                                  new_columns=new_columns,
                                                                  new_index=new_index_column,
                                                                  new_values=new_values)
    result = [item for item in reshaped_table]
    reshaped_table = pd.concat(result)

    # fill NaN values with 0
    reshaped_table = reshaped_table.fillna(0)
    # print(reshaped_table)

    reshaped_corr = reshaped_table.corr()
    # print(reshaped_corr.to_dict())
    yield reshaped_corr


def scatter_operations(query_elem: str, query_value,
                       columns_to_drop: list, source_query: list,
                       source: str, formatter, horizontal: str, vertical: str,
                       column_name: str):
    refined_df = prep_data(query_element=query_elem, query_value=query_value,
                           columns_to_drop=columns_to_drop, source_query=source_query,
                           source=source, df_formatter=formatter)
    refined_result = [item for item in refined_df]
    refined_df = pd.concat(refined_result)

    # filter table for the indicators you want to see on the heatmap
    vals_to_see = [horizontal, vertical]
    new_indicator_table = refined_df[refined_df[column_name].isin(vals_to_see)]

    # enumerate items in the desired new index column
    column_formatter = ColumnFormatter(new_indicator_table['State'])
    target_map = column_formatter.enumerate_column()
    # print(f"New index column successfully enumerated\n\n")

    # replace current values in the column with their mapped enumerated equivalent
    # (it prints a confirmation message if successful)
    state_names = [k for k, v in target_map.items()]

    # state_names = new_indicator_table['State'].copy()
    column_formatter.replace_column_values(target_map=target_map)

    # reshape the table
    reshaped_table = formatter.reshape_table(data_frame=new_indicator_table,
                                             new_columns='Indicator',
                                             new_index='State',
                                             new_values='Value')
    result = [item for item in reshaped_table]
    reshaped_table = pd.concat(result)

    # add states as a new column in the reshaped df
    reshaped_table['State'] = state_names

    # fill NaN values with 0
    reshaped_table = reshaped_table.fillna(0)
    reshaped_table = reshaped_table.reset_index(drop=True)

    print(reshaped_table)
    yield reshaped_table


correlation_formatter = DataFrameFormatter(correlation_input_df)
scatter_formatter = DataFrameFormatter(correlation_input_df)

if __name__ == "__main__":
    scatter_operations(query_elem='Period',
                       query_value=2015,
                       columns_to_drop=['Source', 'Period', 'LGA'],
                       source_query=['NHMIS'],
                       source='Source',
                       formatter=scatter_formatter,
                       vertical='Maternal Mortality Ratio',
                       horizontal='Infant Mortality rate',
                       column_name='Indicator'
                       )

    # correlation_operations(query_elem='Period',
    #                        query_value=2015,
    #                        columns_to_drop=['Source', 'Period', 'LGA'],
    #                        source_query=['NHMIS'],
    #                        source='Source',
    #                        values_to_see=['Infant Mortality rate'],
    #                        new_values='Value',
    #                        new_columns='Indicator',
    #                        new_index_column='State',
    #                        correlation_input_df_formatter=correlation_formatter)
