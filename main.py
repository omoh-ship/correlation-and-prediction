import plotly.express as px
import pandas as pd

xls = pd.ExcelFile("sample_data.xlsx")

correlation_input_df = pd.read_excel(xls, 's')



