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

import spotfire_dsml.time_series.smoothing as tss

@pytest.fixture
def ts_data():
    n_cols = 5
    np.random.seed(10)
    data_dict = {"date": pd.date_range("1/1/2022", "1/25/2022")}
    for i in np.arange(1, n_cols+1):
        data_dict["feature_{}".format(i)] = np.random.normal(size=25)
    data = pd.DataFrame(data_dict)
    return data

def test_warning_on_moving_average_method(ts_data):
    with pytest.warns(UserWarning) as warning_info:
        method = "cumlative"
        tss.moving_average(ts_data["feature_1"], moving_average_type=method)
    assert str(warning_info[0].message) == "moving_average_type not recognized, default 'simple' used."
        
def test_moving_average(ts_data):
    method = "cumulative"
    result = tss.moving_average(ts_data["feature_1"], moving_average_type=method, window_size=2)

    # Test case1: This checks if the given data is of the pandas Dataframe type
    assert isinstance(result, pd.Series), "result should be of type pandas Series"

    # Test case2: This checks if null value is imputed correctly
    assert result[1] == np.mean(ts_data["feature_1"].values[:2])
    
    
def test_warning_on_simple_exponential(ts_data):
    with pytest.warns(UserWarning) as warning_info:
        smoothing_level = 2
        tss.simple_exponential(ts_data["feature_1"], smoothing_level=smoothing_level)
    assert str(warning_info[0].message) == "smoothing_level outside of recommended range of 0-1, use caution when evaluating results."
    
def test_supersmoothing(ts_data):
    index_none = tss.supersmoothing(ts_data["feature_1"])
    index_date = tss.supersmoothing(ts_data["feature_1"], index_col=ts_data["date"])
    
    spaced_ts_data = ts_data.drop(np.arange(1, 5, 2))
    spaced_index_none = tss.supersmoothing(spaced_ts_data["feature_1"])
    spaced_index_date = tss.supersmoothing(spaced_ts_data["feature_1"], index_col=spaced_ts_data["date"])
    
    # Test case1: This checks if the results are the same despite none or date set as index_col
    # we assume this to be true because the dates are evenly spaced
    np.testing.assert_allclose(index_none.values, index_date.values)
    
    # Test case2: This checks if the results are different with none or date set as index_col
    # we assume this to be true because the dates are not evenly spaced
    assert sum(abs(spaced_index_none.values - spaced_index_date.values)) > 0.01

    # Test case3: Fails if data is too small for fit
    with pytest.raises(Exception) as exception_info:
        insuf_ts_data = ts_data.iloc[:5]
        tss.supersmoothing(insuf_ts_data["feature_1"])
    assert "Please make sure there are enough distinct data points to compute the smoother." in str(exception_info.value)
    
    
def test_loess(ts_data):
    index_none = tss.loess(ts_data["feature_1"])
    index_date = tss.loess(ts_data["feature_1"], index_col=ts_data["date"])
    
    spaced_ts_data = ts_data.drop(np.arange(1, 5, 2))
    spaced_index_none = tss.loess(spaced_ts_data["feature_1"])
    spaced_index_date = tss.loess(spaced_ts_data["feature_1"], index_col=spaced_ts_data["date"])
    
    # Test case1: This checks if the results are the same despite none or date set as index_col
    # we assume this to be true because the dates are evenly spaced
    np.testing.assert_allclose(index_none.values, index_date.values)
    
    # Test case2: This checks if the results are different with none or date set as index_col
    # we assume this to be true because the dates are not evenly spaced
    assert sum(abs(spaced_index_none.values - spaced_index_date.values)) > 0.01

    # Test case3: Fails if nulls in index
    with pytest.raises(Exception) as exception_info:
        spaced_ts_data.loc["date", 0] = np.nan
        tss.loess(spaced_ts_data["feature_1"], index_col=spaced_ts_data["date"])
    assert "index_col contains null values. Please remove or replace them before smoothing." in str(exception_info.value)
    
def test_warning_on_fourier(ts_data):
    with pytest.warns(UserWarning) as warning_info:
        pct_to_keep = -1
        tss.fourier(ts_data["feature_1"], pct_to_keep=pct_to_keep)
    assert str(warning_info[0].message) == "pct_to_keep outside of range 0-1, using default of '0.5'"
    
def test_fourier(ts_data):
    pct_dec = tss.fourier(ts_data["feature_1"], 0.25)
    pct_int = tss.fourier(ts_data["feature_1"], 25)
    
    # Test case1: This checks if the results are the same if pct_to_keep is set as a decimal or int
    # this checks whether the fail-safe of converting an int into a pct works
    np.testing.assert_array_equal(pct_dec.values, pct_int.values)
    
def test_kernel(ts_data):
    # Test case1: Fails if kernel typed in wrong
    with pytest.raises(Exception) as exception_info:
        method = "epanecnikov"
        tss.kernel_weighted_average(ts_data["feature_1"], kernel=method)
    assert "Invalid kernel type." in str(exception_info.value)
    
    # Test case1: Fails if nulls exist in measurement_col
    with pytest.raises(Exception) as exception_info:
        null_ts_data = ts_data.copy()
        null_ts_data.loc[1, "feature_1"] = np.nan
        tss.kernel_weighted_average(null_ts_data["feature_1"])
    assert "measurement_col contains null values. Please remove or replace them before smoothing." in str(exception_info.value)