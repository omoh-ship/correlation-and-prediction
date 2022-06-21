import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
from operations import correlation_input_df, scatter_operations, scatter_formatter
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

source_selector = dcc.Dropdown(id='source', options=source_options,
                               value=source_options[0]['value'])

year_dropdown = dcc.Dropdown(id='year', value=2017, clearable=False,
                             options=dropdown_options(correlation_input_df, 'Period'))

indicator_options = dropdown_options(correlation_input_df, 'Indicator')

vertical_selector_label = html.Label(['Select Indicator for Y axis'],
                                     style={'font-weight': 'bold', "text-align": "right", "offset": 1})

vertical_indicator_selector = dcc.Dropdown(id='vertical', options=indicator_options,
                                           value=indicator_options[0]['value'])

horizontal_selector_label = html.Label(['Select Indicator for X axis'],
                                       style={'font-weight': 'bold', "text-align": "right", "offset": 1})

horizontal_indicator_selector = dcc.Dropdown(id='horizontal', options=indicator_options,
                                             value=indicator_options[1]['value'])
graph = dcc.Graph(id='graph', figure={})

app.layout = html.Div(children=[
    source_selector,
    year_dropdown,
    horizontal_selector_label,
    horizontal_indicator_selector,
    vertical_selector_label,
    vertical_indicator_selector,
    graph
])


@app.callback(
    Output('graph', 'figure'),
    Input('source', 'value'),
    Input('year', 'value'),
    Input('vertical', 'value'),
    Input('horizontal', 'value')
)
def cb(source, year, vertical, horizontal):
    df = scatter_operations(query_elem='Period',
                            query_value=year,
                            columns_to_drop=['Source', 'Period', 'LGA'],
                            source_query=[source],
                            source='Source',
                            formatter=scatter_formatter,
                            horizontal=horizontal,
                            vertical=vertical,
                            column_name='Indicator')
    df = [item for item in df]
    df = pd.concat(df)
    # return px.imshow(df)
    # return px.scatter(df, x=horizontal, y=vertical)
    if df.empty:
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

    return px.scatter(df, x=horizontal, y=vertical, trendline='ols', color='State', trendline_scope="overall")


if __name__ == "__main__":
    app.run_server(debug=True)
