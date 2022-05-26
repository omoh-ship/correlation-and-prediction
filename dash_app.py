import plotly.express as px
from dash import dcc, Dash, html
from dash.dependencies import Input, Output
from main import correlation_operations, correlation_input_df
from pandas import DataFrame

my_dict = {'Computer':1500,'Monitor':300,'Printer':150,'Desk':250}
list_1 = ['imr', 'mmr', 'sld']
list_2 = [2002, 2001, 2001]
list_3 = ['edo', 'abia', 'abia']
list_4 = ['north', 'east', 'east']
list_5 = ['uk', 'uk', 'uk']
list_6 = [20, 56, 89]
df = DataFrame(list(zip(list_1, list_2, list_3, list_4, list_5, list_6)),
               columns = ['Indicator','Period','State', 'LGA', 'Source', 'Value'])


def dropdown_options(data_frame:DataFrame, query:str) -> list:
    options = [{'label': year, 'value':year} for year in data_frame[query].unique()]
    return options


app = Dash(__name__)



year_dropdown = dcc.Dropdown(id='year', value=2001, clearable=False,
            options=dropdown_options(correlation_input_df, 'Period'))
graph = dcc.Graph(id='graph', figure={})


app.layout = html.Div(children=[
    year_dropdown,
    graph
])


@app.callback(Output('graph', 'figure'), Input('year', 'value'))
def cb(year):
    data_frame = correlation_operations(data_frame=correlation_input_df, 
                        query_elem='Period',
                        query=year,
                        columns_to_drop=['Source', 'Period', 'LGA'],
                        new_index_column='State',
                        new_columns='Indicator',
                        new_values='Value')
    return px.imshow(data_frame)


if __name__ == "__main__":
    app.run_server(debug=True)

