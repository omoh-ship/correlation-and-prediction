import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
from operations import correlation_operations, correlation_input_df, correlation_formatter
import pandas as pd


def dropdown_options(data_frame: pd.DataFrame, query: str) -> list:
    """
    makes a list of the unique items in a specified dataframe series.
    Args:
        data_frame: the dataframe whose series we are getting unique values
        query: the name of the column we are looking tpo get unique values from
    Return:
        a list of unique values from the column
    """
    options = [{'label': item, 'value': item} for item in data_frame[query].unique()]
    return options


app = Dash(__name__)

source_options = dropdown_options(correlation_input_df, 'Source')
# print(source_options)

source_selector = dcc.Dropdown(id='source', options=source_options,
                               value=source_options[0]['value'])

year_dropdown = dcc.Dropdown(id='year', value=2003, clearable=False,
                             options=dropdown_options(correlation_input_df, 'Period'))

indicator_options = dropdown_options(correlation_input_df, 'Indicator')
# print(indicator_options)

indicator_selector = dcc.Dropdown(id='indicators', options=indicator_options,
                                  multi=True, value=[indicator_options[0]['value'], indicator_options[1]['value']])
graph = dcc.Graph(id='graph', figure={})

app.layout = html.Div(children=[
    source_selector,
    year_dropdown,
    indicator_selector,
    graph
])


@app.callback(
    Output('graph', 'figure'),
    Input('source', 'value'),
    Input('year', 'value'),
    Input('indicators', 'value'))
def cb(source, year, indicators):
    data_frame = correlation_operations(query_elem='Period',
                                        query_value=year,
                                        columns_to_drop=['Source', 'Period', 'LGA'],
                                        new_index_column='State',
                                        new_columns='Indicator',
                                        new_values='Value',
                                        values_to_see=indicators,
                                        source_query=[source],
                                        source='Source',
                                        correlation_input_df_formatter=correlation_formatter)
    data_frame = [item for item in data_frame]
    print(data_frame)
    data_frame = pd.concat(data_frame)
    if not data_frame.empty:
        print(data_frame)
        return px.imshow(data_frame, color_continuous_scale='viridis')

    print("Dataframe is empty")
    return {
        "layout": {
            "xaxis": {
                "visible": False
            },
            "yaxis": {
                "visible": False
            },
            "annotations": [
                {
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        }
    }


if __name__ == "__main__":
    app.run_server(debug=True)
