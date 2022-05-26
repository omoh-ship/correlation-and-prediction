import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
from operations import correlation_operations, correlation_input_df
from pandas import DataFrame


def dropdown_options(data_frame:DataFrame, query:str) -> list:
    options = [{'label': year, 'value':year} for year in data_frame[query].unique()]
    return options


app = Dash(__name__)



year_dropdown = dcc.Dropdown(id='year', value=2003, clearable=False,
            options=dropdown_options(correlation_input_df, 'Period'))
graph = dcc.Graph(id='graph', figure={})


app.layout = html.Div(children=[
    year_dropdown,
    graph
])


@app.callback(Output('graph', 'figure'), Input('year', 'value'))
def cb(year):
    data_frame = correlation_operations(table=correlation_input_df, 
                        query_element='Period',
                        query_value=year,
                        columns_to_drop=['Source', 'Period', 'LGA'],
                        new_index_column='State',
                        new_columns='Indicator',
                        new_values='Value')
    return px.imshow(data_frame)


if __name__ == "__main__":
    app.run_server(debug=True)

