import pandas as pd
from predictive_model_functions import differencer, arima_value_generator, is_stationary, column_dropper, \
    arima_forecast, is_empty, index_setter, filter_df
from statsmodels.tsa.stattools import adfuller

xls = pd.ExcelFile("data/sample_data.xlsx")
CORRELATION_INPUT_DF = pd.read_excel(xls, "Correlation Input Sheet")


# print(CORRELATION_INPUT_DF.head())


def prediction_operation(dataframe: pd.DataFrame, indicator_column: str,
                         indicator_query: str, state_column: str, state_query: str,
                         source_column: str, source_query: str, columns_to_drop: list,
                         period_column: str, values_column: str, forecast_years: list):
    """
    Args:
         dataframe: the dataframe to be worked on.
         indicator_column: the name of the column with the indicators.
         indicator_query: the indicator to filter the indicator_column by.
         state_column: the name of the column with the states.
         state_query: the state to filter the state_column by.
         source_column: the name of the column with the data sources.
         source_query: the source to filter the source_column by.
         columns_to_drop: list of columns to be dropped for the operation to work.
         period_column: the column with time e.g years, months.
         values_column: the column with the values to be used in prediction.
         forecast_years: the list of the years you want a forecast for

    Returns:
        a generator
    """
    for year in forecast_years:

        # filter df
        correlation_df = filter_df(dataframe, indicator_column, indicator_query,
                                   state_column, state_query, source_column, source_query)
        correlation_df = [item for item in correlation_df]

        # checks if the list containing the df is empty
        if is_empty(correlation_df):
            return correlation_df
        # if the items in generator are empty return
        correlation_df = pd.concat(correlation_df)

        # drop columns that won't help prediction'
        correlation_df = column_dropper(correlation_df, columns_to_drop)
        correlation_df = [item for item in correlation_df]
        correlation_df = pd.concat(correlation_df)

        # make the figures in the Period column datetime objects
        correlation_df[period_column] = pd.to_datetime(correlation_df[period_column], format='%Y')

        # set Period to be the new index of the df
        correlation_df = index_setter(correlation_df, period_column)
        correlation_df = [item for item in correlation_df]
        correlation_df = pd.concat(correlation_df)

        # store the value column in a variable called values
        values = correlation_df[values_column]
        result = adfuller(values)
        p_val = result[1]

        # check if data is stationary by evaluating p value from adfuller test
        if not is_stationary(p_val):
            differenced_df = differencer(df=correlation_df, values_column=values_column, p_val=p_val)
            differenced_df = [item for item in differenced_df]
            # try with next() then time the code and see if it goes faster
            # differenced_df = [item.next() for item in differenced_df]x
            differenced_df = pd.concat(differenced_df)
            correlation_df = differenced_df.dropna()

        fit = arima_value_generator(correlation_df[values_column])
        predicted_df = arima_forecast(fit=fit, series_forecast=correlation_df[values_column],
                                      year=year, original_df=dataframe,
                                      indicator_query=indicator_query, state_query=state_query,
                                      source_query=source_query)
        predicted_df = [item for item in predicted_df]
        dataframe = pd.concat(predicted_df)
        # else:
        #     return "empty"
    # filter the final df
    final_filtered_df = filter_df(dataframe, indicator_column, indicator_query,
                                  state_column, state_query, source_column, source_query)
    final_filtered_df = [item for item in final_filtered_df]
    final_filtered_df = pd.concat(final_filtered_df)

    # drop useless columns from the final df
    final_filtered_df = column_dropper(final_filtered_df, columns_to_drop)
    final_filtered_df = [item for item in final_filtered_df]
    final_filtered_df = pd.concat(final_filtered_df)

    # make the figures in the Period column datetime objects
    final_filtered_df[period_column] = pd.to_datetime(final_filtered_df[period_column], format='%Y')

    # set Period to be the new index of the df
    final_filtered_df = index_setter(final_filtered_df, period_column)

    return final_filtered_df


prediction_operation(dataframe=CORRELATION_INPUT_DF,
                     indicator_column='Indicator',
                     indicator_query='Infant Mortality rate',
                     state_column='State',
                     state_query='Abia',
                     source_column='Source',
                     source_query='NHIS',
                     columns_to_drop=['Indicator', 'State', 'LGA', 'Source'],
                     period_column='Period',
                     values_column='Value',
                     forecast_years=[2017, 2018]
                     )
