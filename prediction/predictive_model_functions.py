import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller


def is_stationary(p_val):
    """
    checks if the p_value to determine if the data is stationary.
    Args:
        p_val: the p_value to be checked.
    Returns:
        boolean

    """
    if p_val > 0.05:
        return False
    else:
        return True


def differencer(df, values_column, p_val):
    """
    Differences the data until it becomes stationary.
    Args:
        df: the dataframe to be differenced.
        values_column: the column that has the initial values used for the adfuller test
        p_val: the p_value gotten from the first adfuller test

    """
    differencing_num = 0

    # run while the data is not stationary
    while not is_stationary(p_val):
        differencing_num += 1

        # Moving the data by first difference.
        if differencing_num < 2:
            df[f'{differencing_num}difference'] = df[values_column] - df[values_column].shift(1)

        # Move the data by any other difference
        else:
            df[f'{differencing_num}difference'] = df[f'{differencing_num - 1}difference'] - df[
                f'{differencing_num - 1}difference'].shift(1)
            # print(f"completed shift {differencing_num}")

        p_val = adfuller(df[f'{differencing_num}difference'].dropna())[1]

        # check if data has now become stationary
        if is_stationary(p_val):
            yield df


def arima_value_generator(values: pd.Series,
                        #   start_p, start_q, max_p, max_q, d,
                        # m=12, start_P=0, seasonal=False, D=None,
                          trace=True,
                          error_action='ignore', suppress_warnings=True,
                          stepwise=True):
    """
    A function that makes a forecast using a auto_arima to get the best
    p, d and q values to use in the ARIMA model
    Args:
        values: Column to be used for prediction
        start_p: starting autoregressor
        start_q: starting moving average
        max_p: max autoregressor
        max_q: max moving average
        m:
        d: differencing term-int
        start_P:
        seasonal: if data is seasonal
        D:
        trace:
        error_action:
        suppress_warnings:
        stepwise:

    """
    stepwise_fit = auto_arima(values,
                              trace=trace,
                              error_action=error_action,
                              suppress_warnings=suppress_warnings,
                              stepwise=stepwise)
    return stepwise_fit


def arima_forecast(fit, series_forecast, year,
                   original_df, indicator_query,
                   state_query, source_query
                   ):
    """
    A function that makes a forecast using a ARIMA
    Args:
        fit: stepwise_fit obtained from arima_value_checker
        series_forecast: the column to be used for forecasting-pandas.Series
        original_df: data frame to add new predicted values to
        indicator_query: the indicator used to filter the original df
        state_query: the state used to filter the original df
        source_query: the source used to filter the original df
        year: year being forecast
    """
    X = series_forecast.values
    X = X.astype('float32')
    existing_years = series_forecast.index.year

    history = [value for value in X]
    model = ARIMA(history, order=fit.get_params()['order'])
    model_fit = model.fit()
    y_hat = model_fit.forecast()[0]

    if year not in existing_years:
        print('For Year %d --> Predicted = %.3f' % (year, y_hat))

        original_df.loc[len(original_df.index)] = [indicator_query, year, state_query, 'All', source_query, y_hat]
        # 2018 and 19 are giving the same values check this with tobi
        # print(original_df.tail())
        yield original_df
    else:
        print(f"\nThe value for the year {year} you are trying to predict already exists\n")
        yield original_df


def sheet_splitter(example_sheet, query_column, query):
    """
    a function that checks if a query is present in an example sheet,
    splits the example sheet based on the provided query in the query_column and then,
    outputs a CSV file and determines whether time series forecasts,
    can be performed on the split data. Expects at least 15 data points,
    to pass check

    Args:
    example_sheet: dataframe to be filtered-pandas dataframe
    query_column: the column the query should be searched in-string
    query: what will be used to filter the passed in dataframe-string.

    Return:
    result_df-dataFrame
    """

    # Declare the query conditional
    query_conditional = example_sheet[query_column] == query

    result_df = example_sheet[query_conditional]

    # Determine how many data points are suitable for data forecasting
    if len(result_df) >= 15:
        print(f"{query_column} : {query}, with length: {len(result_df)} can be forecast")
        yield result_df

    else:
        return f"""{query_column} : {query} with length: {len(result_df)}, cannot be forecast, choose another indicator or check spelling"""

