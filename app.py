import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output

app = Dash(__name__)



def main(data_frame, query, app):
    app.layout = html.Div(children=[
        dcc.Dropdown(id='year', value=2001, clearable=False,
            options=[{'label': year, 'value':year} for year in data_frame[query].unique()]),
        dcc.Graph(id='graph', figure={})

    ])


@app.callback(Output('graph', 'figure'), Input('year', 'value'))
def cb(year):
    df = correlation_operations(data_frame=correlation_input_df, 
                        query_elem='Period',
                        query=year,
                        columns_to_drop=['Source', 'Period', 'LGA'],
                        new_index_column='State',
                        new_columns='Indicator',
                        new_values='Value')
    return px.imshow(df)


if __name__ == "__main__":
    app.run_server(debug=True)

