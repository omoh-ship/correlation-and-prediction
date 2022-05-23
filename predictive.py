import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

xls = pd.ExcelFile("sample_data.xlsx")
correlation_input_df = pd.read_excel(xls, 'Correlation Input Sheet', parse_dates=['Period'], index_col='Period')


def sheet_splitter(example_sheet, indicator):
    """
    a function that checks if an indicator is present in an example sheet,
    splits the example sheet based on the provided indicator and then,
    outputs a CSV file and determines whether time series forecasts,
    can be performed on the split data. Expects at least 15 data points,
    to pass check.
    Args:
        example_sheet-pandas dataframe
        indicator-string
    Returns:
        indicator_df-dataframe, Information on the split file for forecasting.
    """

    # Declare the indicator conditional
    indicator_conditional = example_sheet['Indicator'] == indicator

    # Make of copy of a slice of the original dataframe
    indicator_df = example_sheet[indicator_conditional].copy()

    # Determine how many data points are suitable for data forecasting
    if len(indicator_df) >= 15:
        print(f"Indicator : {indicator}, with length: {len(indicator_df)} can be forecast")
        return indicator_df

    else:
        print(f"Indicator : {indicator} with length: {len(indicator_df)}, "
              "cannot be forecast, choose "
              "another indicator or check spelling")



def arima_forecast(dataframe, year, p=0, d=1, q=0):
    """
    A function that makes a forecast using a ARIMA and evaluates
    the model with RMSE.
    Args:
        dataframe-pandas: series
        p: autoregressor term-int
        d: differencing term-int
        q: moving average term-int
        year: year being forecast
    """
    series_forecast = dataframe.drop(['Indicator', 'State', 'LGA', 'Source'], axis=1)

    X = series_forecast.values

    X = X.astype('float32')

    history = [value for value in X]

    model = ARIMA(history, order=(0, 0, 0))
    model_fit = model.fit()

    y_hat = model_fit.forecast()[0]

    print('For Year %d --> Predicted = %.3f' % (year, y_hat))



arima_forecast(correlation_input_df, 2005, p=1, d=1, q=0)
