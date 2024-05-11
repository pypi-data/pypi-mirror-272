import numpy as np
import pandas as pd
import pytest
import sys
import os
from pathlib import Path

# Get the current working directory
current_dir = Path(os.getcwd())

# Assuming the current directory is tests/time_series or a subdirectory of the project
# Adjust the number of parent calls as needed based on your actual directory structure
project_root = current_dir.parent.parent

# Add the project root to sys.path
sys.path.append(str(project_root))

import spotfire_dsml.time_series.forecasting as tsf

@pytest.fixture
def sample_data():
    # Define the start date, number of periods, and frequency
    start_date = "2022-01-01"
    num_periods = 365
    date_range = pd.date_range(start=start_date, periods=num_periods, freq='D')

    # Simulate a linear trend
    linear_trend = np.linspace(start=0, stop=num_periods/10, num=num_periods)

    # Simulate a seasonal component (e.g., sine wave for yearly seasonality)
    seasonality = 10 * np.sin(np.linspace(start=0, stop=2*np.pi, num=num_periods))

    # Add random noise
    np.random.seed(42)  # Seed for reproducibility
    noise = np.random.normal(loc=0, scale=2, size=num_periods)

    # Combine the components to create the time series
    data = linear_trend + seasonality + noise

    # Create a DataFrame
    measurement_col = pd.Series(data, name="Measurement")
    return measurement_col

def test_lstm(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    lookback = 2
    neurons = 200
    batch_size = 32
    epochs = 50
    dropout = 0.5
    test_size = 0.2
    index_col = None

    # Call the lstm function
    result = tsf.lstm(sample_data, n_ahead, lookback, neurons, batch_size, epochs, dropout, test_size, index_col)

    # Check the shape of the result
    assert result.shape == (n_ahead, 2)

    # Check if the forecasted values are within the expected range
    assert np.all(result[sample_data.name] >= np.min(sample_data))
    assert np.all(result[sample_data.name] <= np.max(sample_data))

    # Check if the index column is generated correctly
    if index_col is not None:
        assert result.columns[0] == index_col.name
    
def test_arima(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    max_p = 4
    max_q = 2
    max_d = 2
    conf_lvl = 0.95
    index_col = None

    # Call the arima function
    result = tsf.arima(sample_data, n_ahead, max_p, max_q, max_d, conf_lvl, index_col)

    # Check the shape of the result
    assert result.shape == (n_ahead, 4)

    # Check if the forecasted values are within the expected range
    assert np.all(result[sample_data.name] >= np.min(sample_data))
    assert np.all(result[sample_data.name] <= np.max(sample_data))

    # Check if the index column is generated correctly
    if index_col is not None:
        assert result.columns[0] == index_col.name

def test_holt_winters(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    seasonal_freq = 60
    seasonal_type = 'add'
    trend_type = None
    conf_lvl = 0.5
    damped = None
    index_col = None
    
    # Call the holt_winters function
    result = tsf.holt_winters(sample_data, n_ahead, seasonal_freq, seasonal_type, trend_type,
                              conf_lvl, damped, index_col)

    # Check the shape of the result
    assert result.shape == (n_ahead, 4)

    # Check if the forecasted values are within the expected range
    assert np.all(result[sample_data.name] >= np.min(sample_data))
    assert np.all(result[sample_data.name] <= np.max(sample_data))

    # Check if the index column is generated correctly
    if index_col is not None:
        assert result.columns[0] == index_col.name
        
def test_lstm_lookback_error(sample_data):
    # Set the parameters for testing
    n_ahead = 200
    lookback = 200
    neurons = 200
    batch_size = 32
    epochs = 50
    dropout = 0.5
    test_size = 0.2
    index_col = None

    # Raise error when lookback is too high
    with pytest.raises(Exception) as exception_info:
        result = tsf.lstm(sample_data, n_ahead, lookback, neurons, batch_size, epochs, dropout, test_size, index_col)
    assert "lookback must be less than the test set size" in str(exception_info.value)

def test_arima_int_index(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    max_p = 4
    max_q = 2
    max_d = 2
    conf_lvl = None
    index_col = np.arange(0, len(sample_data) * 3, 3)

    # Call the arima function
    result = tsf.arima(sample_data, n_ahead, max_p, max_q, max_d, conf_lvl, index_col)

    # Check the shape of the result
    assert result.shape == (n_ahead, 2)

    # Check if the new index is larger than the input index
    assert np.all(result["index"] >= np.max(index_col))
        
def test_holt_winters_damped(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    seasonal_freq = 60
    seasonal_type = 'add'
    trend_type = None
    conf_lvl = 0.5
    damped = True
    index_col = None
        
    # Raise error when damped is True, but trend_type is None
    with pytest.raises(Exception) as exception_info:
        result = tsf.holt_winters(sample_data, n_ahead, seasonal_freq, seasonal_type, trend_type, conf_lvl, damped, index_col)
    assert "Can only dampen the trend component" in str(exception_info.value)
    
def test_holt_winters_seasonal_freq(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    seasonal_freq = 200
    seasonal_type = 'add'
    trend_type = None
    conf_lvl = 0.5
    damped = False
    index_col = None
        
    # Raise error when seasonal_freq is too high; there needs to be 2 * seasonal freq values to work
    with pytest.raises(Exception) as exception_info:
        result = tsf.holt_winters(sample_data, n_ahead, seasonal_freq, seasonal_type, trend_type, conf_lvl, damped, index_col)
    assert "Cannot compute initial seasonals using heuristic method with less than two full seasonal cycles" in str(exception_info.value)

def test_lstm_nulls(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    lookback = 2
    neurons = 200
    batch_size = 32
    epochs = 50
    dropout = 0.5
    test_size = 0.2
    index_col = None
    sample_data[1:6] = np.nan

    # Raise error when there are nulls
    with pytest.raises(Exception) as exception_info:
        result = tsf.lstm(sample_data, n_ahead, lookback, neurons, batch_size, epochs, dropout, test_size, index_col)
    assert "measurement_col contains null values" in str(exception_info.value)

def test_lstm_invalid_freq(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    lookback = 2
    neurons = 200
    batch_size = 32
    epochs = 50
    dropout = 0.5
    test_size = 0.2
    index_col = np.arange(len(sample_data))
    index_col = np.delete(index_col, np.arange(1, 7))
    sample_data[1:6] = np.nan
    sample_data = sample_data.dropna()

    # Raise error when frequency is abnormal
    with pytest.raises(Exception) as exception_info:
        result = tsf.lstm(sample_data, n_ahead, lookback, neurons, batch_size, epochs, dropout, test_size, index_col)
    assert "Frequency could not be determined" in str(exception_info.value)
    
def test_arima_nulls(sample_data):
    # Set the parameters for testing
    n_ahead = 3
    max_p = 4
    max_q = 2
    max_d = 2
    conf_lvl = 0.95
    index_col = None
    sample_data[1:6] = np.nan
    
    # Raise error when arima has nulls
    with pytest.raises(Exception) as exception_info:
        result = tsf.arima(sample_data, n_ahead, max_p, max_q, max_d, conf_lvl, index_col)
    assert "measurement_col contains null values" in str(exception_info.value)