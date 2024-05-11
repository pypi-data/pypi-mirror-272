import pandas as _pd
import numpy as _np
import warnings as _warnings
from statsmodels.tsa.stattools import adfuller as _adfuller, arma_order_select_ic as _arma_order_select_ic
from statsmodels.tsa.arima.model import ARIMA as _ARIMA
from statsmodels.tsa.exponential_smoothing.ets import ETSModel as _ETSModel
from tensorflow.keras.models import Sequential as _Sequential
from tensorflow.keras.layers import Dense as _Dense, LSTM as _LSTM, Dropout as _Dropout
from sklearn.metrics import mean_squared_error as _mean_squared_error

# Function to find optimal d
def _find_d(time_series, max_d=2):
    d = 0
    adf_result = _adfuller(time_series)
    while adf_result[1] > 0.05:  # p-value > 0.05 implies non-stationarity
        d += 1
        if d > max_d:
            _warnings.warn("Warning: not able to make time series stationary. Please consider other methods and/or increase max_d")
            return 0
        adf_result = _adfuller(_np.diff(time_series, n=d))
    return d

# Function to find optimal p, q
def _find_p_q(time_series, max_p, max_q):
    order = _arma_order_select_ic(time_series, ic='aic', max_ar=max_p, max_ma=max_q, trend='c')
    p = order.aic_min_order[0]
    q = order.aic_min_order[1]
    return p, q

def arima(measurement_col, n_ahead, max_p=4, max_q=2, max_d=2, conf_lvl=None, index_col=None):
    """
    Uses ARIMA to forecast future values of a measurement column. Well-suited for forecasting data where trends and
    patterns emerge over time, even when these don't follow a seasonal cycle. Incorporates autoregression (AR),
    differencing to achieve stationarity (I), and moving average (MA) components to capture the autocorrelation within
    the series.
    
    Parameters
    ----------
    measurement_col : array-like
        The measurement column for which to forecast future values.
    
    n_ahead : int
        The number of time steps to forecast into the future.

    max_p : int, optional (default=4)
        Maximum value for p (AR) to test when finding its optimal value, as selected by AIC.
        p defines the number of previous values to use when predicting the current value.

    max_q : int, optional (default=2)
        Maximum value for q (MA) to test when finding its optimal value, as selected by AIC.
        q defines the number of previous errors to incorporate in the MA model.
        
    max_d : int, optional (default=2)
        Maximum value for d (I) to test when finding its appropriate value. d determines the number of 
        times the time series is differenced in order for the time series to be stationary. In practice,
        it is seldom necessary to go beyond second-order differences [1].

    conf_lvl : float, optional (default=None)
        The confidence level for the prediction intervals. If None, no prediction intervals will be calculated.
        Must be between 0 and 1.

    index_col : array-like, optional (default=None)
        The index of the input data. If None, an evenly spaced integer index is created.
        Supports datetime.date, datetime.datetime, datetime.time, and integer data types.

    Returns
    -------
    pandas DataFrame : A table containing the forecasted values of measurement_col, along with an index; 
        optionally includes columns with the confidence intervals
        

    References
    ----------
    
    [1]
    Hyndman, R.J., & Athanasopoulos, G. (2018) Forecasting: principles and practice, 2nd edition, OTexts:
    Melbourne, Australia. OTexts.com/fpp2/stationarity.html. Accessed on Feb 21st, 2024.
        
    """
    index_col_int = False
    
    try:
        measurement_col_name = measurement_col.name
    except:
        measurement_col_name = "Measurement"
        measurement_col = _pd.Series(measurement_col, name=measurement_col_name)
        
    if _np.any(_pd.isnull(measurement_col)):
        raise ValueError("measurement_col contains null values. Please remove or replace them before forecasting.")

    if index_col is not None:
        inferred_freq = _pd.infer_freq(index_col)
        if inferred_freq == None:
            raise ValueError("Frequency could not be determined. Please check if index frequency is irregular or if there are missing values that break the frequency pattern.")
        if "N" in inferred_freq and index_col.dtype.kind in "iu":
            index_col_int = True

    # Assuming you have a time_series variable
    d = _find_d(measurement_col, max_d)
    if d > 0:
        differenced_col = measurement_col.diff(d).dropna()
    else:
        differenced_col = measurement_col
    p, q = _find_p_q(differenced_col, max_p, max_q)
    print("parameters used: ", p, d, q)
    
    # Fit ARIMA model
    model = _ARIMA(measurement_col, order=(p, d, q))
    model_fit = model.fit()
    
    # Forecast
    if conf_lvl:
        measurement_len = len(measurement_col)
        forecast_df = model_fit.get_prediction(start=measurement_len+1, 
                                               end=measurement_len+n_ahead).summary_frame(alpha=1-conf_lvl)
        forecast_df = forecast_df.rename(columns={"mean": measurement_col_name,
                                                  "mean_ci_lower": "{}_ci_lower".format(measurement_col_name),
                                                  "mean_ci_upper": "{}_ci_upper".format(measurement_col_name)}).drop("mean_se", axis=1)
    else:
        forecast_df = model_fit.forecast(steps=n_ahead).rename(measurement_col_name)
    
    # if there is a provided index, add n_ahead time steps to it and assign it to the forecast_df index
    if index_col is not None:
        if not isinstance(index_col, _pd.Series):
            index_col_name = "index"
            index_col = _pd.Series(index_col, name=index_col_name)
        last_index_value = index_col.iloc[-1]
        if index_col_int:
            step_size = 1 if inferred_freq == "N" else int(inferred_freq.replace("N", ""))
            forecast_df.index = _np.arange(last_index_value + step_size, last_index_value + (step_size * (n_ahead + 1)), step_size)
        else:
            forecast_df.index = _pd.date_range(start=last_index_value, periods=n_ahead + 1, freq=inferred_freq)[1:]
        forecast_df.index.name = index_col.name

    return forecast_df.reset_index()


def holt_winters(measurement_col, n_ahead, seasonal_freq, seasonal_type="add", trend_type="add", conf_lvl=None, damped=False, index_col=None):
    """
    Uses Holt-Winters to forecast future values of a measurement column. Ideal for univariate time series with a clear
    seasonal pattern and trend, leveraging smoothing techniques to adjust for seasonality, trend, and level in the data.
    
    Parameters
    ----------
    measurement_col : array-like
        The measurement column for which to forecast future values.
    
    n_ahead : int
        The number of time steps to forecast into the future.
        
    seasonal_freq : int
        The number of observations per seasonal cycle. For example, if the data is monthly, then freq=12.
    
    seasonal_type : str, optional (default="add")
        Specifies the seasonal component type. 
        Options:
        "add" - additive, suitable when seasonal variations are roughly constant
        "mul" - multiplicative, suitable when seasonal variations change proportionally to the level of the series
        None - no seasonality

    trend_type : str, optional (default="add")
        Specifies the trend component type.
        Options:
        "add" - additive, suitable when the series has linear trends
        "mul" - multiplicative, suitable when the series grows or declines at a non-linear rate
        None - no trend

    conf_lvl : float, optional (default=None)
        The confidence level for the prediction intervals. If None, no prediction intervals will be calculated.
        Must be between 0 and 1.
        
    damped : boolean, optional (default=False)
        Indicates if damping is applied to reduce the trend component over time for more conservative forecasts.
        
    index_col : array-like, optional (default=None)
        The index of the input data. If None, an evenly spaced integer index is created.
        Supports datetime.date, datetime.datetime, datetime.time, and integer data types.

    Returns
    -------
    pandas DataFrame : A table containing the forecasted values of measurement_col, along with an index; 
        optionally includes columns with the confidence intervals
        
    """
    index_col_int = False
    
    try:
        measurement_col_name = measurement_col.name
    except:
        measurement_col_name = "Measurement"
        measurement_col = _pd.Series(measurement_col, name=measurement_col_name)
        
    if _np.any(_pd.isnull(measurement_col)):
        raise ValueError("measurement_col contains null values. Please remove or replace them before forecasting.")
    
    if index_col is not None:
        inferred_freq = _pd.infer_freq(index_col)
        if inferred_freq == None:
            raise ValueError("Frequency could not be determined. Please check if index frequency is irregular or if there are missing values that break the frequency pattern.")
        if "N" in inferred_freq and index_col.dtype.kind in "iu":
            index_col_int = True
    
    # Build model
    ets_model = _ETSModel(
        endog=measurement_col,
        seasonal=seasonal_type,
        seasonal_periods=seasonal_freq,
        trend=trend_type,
        damped_trend=damped
    )
    ets_result = ets_model.fit()
    
    # Forecast
    if conf_lvl:
        measurement_len = len(measurement_col)
        forecast_df = ets_result.get_prediction(start=measurement_len+1,
                                                end=measurement_len+n_ahead).summary_frame(alpha=1-conf_lvl)
        forecast_df = forecast_df.rename(columns={"mean": measurement_col_name,
                                                  "pi_lower": "{}_ci_lower".format(measurement_col_name),
                                                  "pi_upper": "{}_ci_upper".format(measurement_col_name)})
    else:
        forecast_df = ets_result.forecast(steps=n_ahead).rename(measurement_col_name)
    
    # if there is a provided index, add n_ahead time steps to it and assign it to the forecast_df index
    if index_col is not None:
        if not isinstance(index_col, _pd.Series):
            index_col_name = "index"
            index_col = _pd.Series(index_col, name=index_col_name)
        last_index_value = index_col.iloc[-1]
        if index_col_int:
            step_size = 1 if inferred_freq == "N" else int(inferred_freq.replace("N", ""))
            forecast_df.index = _np.arange(last_index_value + step_size, last_index_value + (step_size * (n_ahead + 1)), step_size)
        else:
            forecast_df.index = _pd.date_range(start=last_index_value, periods=n_ahead + 1, freq=inferred_freq)[1:]
        forecast_df.index.name = index_col.name

    return forecast_df.reset_index()

def _create_dataset(dataset, lookback=1):
    dataX, dataY = [], []
    for i in _np.arange(len(dataset)-lookback):
        a = dataset[i:(i+lookback), 0]
        dataX.append(a)
        dataY.append(dataset[i+lookback, 0])
    return _np.array(dataX), _np.array(dataY)
    
def lstm(measurement_col, n_ahead, lookback, neurons=200, batch_size=32, epochs=50, dropout=0.5, test_size=0.2, index_col=None):
    """
    Uses LSTM (Long Short-Term Memory) networks to forecast future values of a measurement column. Well-adapted for a wide
    range of univariate time series, including those with complex patterns that may not be well-captured by traditional
    methods. LSTM excels in learning from long-term dependencies, making it effective for data with large seasonal patterns
    or when capturing subtler trends and relationships is crucial.

    Parameters
    ----------
    measurement_col : array-like
        The measurement column for which to forecast future values.

    n_ahead : int
        The number of time steps to forecast into the future.

    lookback : int
        The number of previous time steps to use as input variables to predict the next time period.

    neurons : int, optional (default=200)
        The number of LSTM units in the LSTM layer of the neural network.

    batch_size : int, optional (default=32)
        The number of samples per gradient update in the training phase.

    epochs : int, optional (default=50)
        The number of epochs to train the model. An epoch is an iteration over the entire training data.

    dropout : float, optional (default=0.5)
        The dropout rate for regularization, specifying the fraction of the units to drop for the linear transformation of the inputs.

    test_size : float, optional (default=0.2)
        The proportion of the dataset to include in the test split. The value should be between 0 and 1.
    
    index_col : array-like, optional (default=None)
        The index of the input data. If None, an evenly spaced integer index is created.
        Supports datetime.date, datetime.datetime, datetime.time, and integer data types.

    Returns
    -------
    pandas DataFrame : A table containing the forecasted values of measurement_col, along with an index.
        
    """
    index_col_int = False
    
    try:
        measurement_col_name = measurement_col.name
    except:
        measurement_col_name = "Measurement"
        measurement_col = _pd.Series(measurement_col, name=measurement_col_name)
        
    if _np.any(_pd.isnull(measurement_col)):
        raise ValueError("measurement_col contains null values. Please remove or replace them before forecasting.")
    
    if index_col is not None:
        inferred_freq = _pd.infer_freq(index_col)
        if inferred_freq == None:
            raise ValueError("Frequency could not be determined. Please check if index frequency is irregular or if there are missing values that break the frequency pattern.")
        if "N" in inferred_freq and index_col.dtype.kind in "iu":
            index_col_int = True

    # load the dataset 
    dataframe = _pd.DataFrame({measurement_col.name: measurement_col})
    dataset = dataframe.values.astype("float")

    # split into train and test sets
    train_size = min(int(len(dataset) * (1 - test_size)), len(dataset) - n_ahead)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    if lookback >= test_size:
        raise ValueError("lookback must be less than the test set size. Please either reduce the lookback value or increase the test_size value.")

    X_train, y_train = _create_dataset(train, lookback)
    X_test, y_test = _create_dataset(test, lookback)
    
    # reshape input to be [samples, time steps, features]
    X_train = _np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = _np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # create and fit the LSTM network
    model = _Sequential()
    model.add(_LSTM(neurons, activation="relu", input_shape=(1, lookback)))
    model.add(_Dropout(dropout))
    model.add(_Dense(1))
    model.compile(loss="mean_squared_error", optimizer="adam")
    # Train the LSTM model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)

    # make predictions
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    train_score = _np.sqrt(_mean_squared_error(y_train, train_predict))
    print("Train Score: %.2f RMSE" % (train_score))
    test_score = _np.sqrt(_mean_squared_error(y_test, test_predict))
    print("Test Score: %.2f RMSE" % (test_score))

    # forecast
    X_new = test[-lookback:]
    for step_ahead in range(n_ahead):
        y_pred_one = model.predict(X_new[step_ahead:].reshape(1, 1, lookback))
        X_new = _np.concatenate([X_new, y_pred_one])
    X_new = X_new[lookback:]
    forecast_df = _pd.DataFrame({measurement_col.name: X_new[:, 0]}, 
                               index=_np.arange(len(measurement_col)+1, len(measurement_col)+1+len(X_new)))

    # if there is a provided index, add n_ahead time steps to it and assign it to the forecast_df index
    if index_col is not None:
        if not isinstance(index_col, _pd.Series):
            index_col_name = "index"
            index_col = _pd.Series(index_col, name=index_col_name)
        last_index_value = index_col.iloc[-1]
        if index_col_int:
            step_size = 1 if inferred_freq == "N" else int(inferred_freq.replace("N", ""))
            forecast_df.index = _np.arange(last_index_value + step_size, last_index_value + (step_size * (n_ahead + 1)), step_size)
        else:
            forecast_df.index = _pd.date_range(start=last_index_value, periods=n_ahead + 1, freq=inferred_freq)[1:]
        forecast_df.index.name = index_col.name
        
    return forecast_df.reset_index()