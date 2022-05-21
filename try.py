import plotly.express as px
import pandas as pd
from column_formatter import ColumnFormatter

xls = pd.ExcelFile("sample_data.xlsx")

correlation_input_df = pd.read_excel(xls, 'Correlation Input Sheet')

def correlation_operations(data_frame:pd.DataFrame, query_elem, query):
    data_frame = data_frame.copy()

correlation_input_df.copy
