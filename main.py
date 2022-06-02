import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
from operations import correlation_operations, correlation_input_df
from pandas import DataFrame


def dropdown_options(data_frame:DataFrame, query:str) -> list:
    options = [{'label': item, 'value':item} for item in data_frame[query].unique()]
    return options


app = Dash(__name__)



year_dropdown = dcc.Dropdown(id='year', value=2011, clearable=False,
            options=dropdown_options(correlation_input_df, 'Period'))

indicator_options = dropdown_options(correlation_input_df, 'Indicator')
# print(indicator_options)
indicator_selector = dcc.Dropdown(id='indicators', options=indicator_options,
                 multi=True, value=[indicator_options[0]['value'], indicator_options[1]['value']])
graph = dcc.Graph(id='graph', figure={})


app.layout = html.Div(children=[
    year_dropdown,
    indicator_selector,
    graph
])


@app.callback(
    Output('graph', 'figure'), 
    Input('year', 'value'), 
    Input('indicators', 'value'))
def cb(year, indicators):
    data_frame = correlation_operations(table=correlation_input_df, 
                        query_element='Period',
                        query_value=year,
                        columns_to_drop=['Source', 'Period', 'LGA'],
                        new_index_column='State',
                        new_columns='Indicator',
                        new_values='Value',
                        values_to_see=indicators)
    return px.imshow(data_frame, color_continuous_scale='viridis')


if __name__ == "__main__":
    app.run_server(debug=True)

