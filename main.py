import plotly.express as px
import pandas as pd
from column_formatter import ColumnFormatter

xls = pd.ExcelFile("sample_data.xlsx")

correlation_input_df = pd.read_excel(xls, 'Correlation Input Sheet')


def table_query(data_frame:pd.DataFrame, query_elem, query):
    """
    Queries the table using tje parameters passed in e.g, data_frame=correlation_input_df,query_elem='Period', query=2001. Therefore correlation_input_df['Period]
    """
    data_frame = data_frame.copy()
    query_result = data_frame[data_frame[query_elem] == query]
    return query_result


def analysis_prep(data_frame:pd.DataFrame, column_names:list):
    """Drop columns that you don't want in your analysis since they probably don't aid it"""
    analysis_prepped_df = data_frame.drop(column_names, axis=1)
    return analysis_prepped_df


# def correlation_operations(data_frame:pd.DataFrame, query_elem, query, columns_to_drop:list):
#     # Query table
#     filter_table = table_query(data_frame=data_frame, query_elem=query_elem, query=query)

#     # drop useless columns
#     refined_df = analysis_prep(data_frame=filter_table, column_names=columns_to_drop)

new = correlation_input_df[correlation_input_df['Period'] == 2001]
print(new)
# correlation_input_df.copy


