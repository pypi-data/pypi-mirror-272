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

import spotfire_dsml.time_series.preprocessing as tsp

@pytest.fixture
def ts_data():
    n_cols = 5
    np.random.seed(10)
    data_dict = {"date": pd.date_range("1/1/2022", "1/5/2022")}
    for i in np.arange(1, n_cols+1):
        data_dict["feature_{}".format(i)] = np.random.normal(size=5)
    data = pd.DataFrame(data_dict)
    data.iloc[1, 1] = np.nan
    data.iloc[2, 2] = np.nan
    return data

def test_exception_on_numeric_imputation_method(ts_data):
    try:
        method = "prevoius"
        with pytest.raises(Exception) as exception_info:
            tsp.missing_value_imputation(ts_data, "Date", numeric_method=method)
            assert exception_info.match(
                "Exception: numeric_method not recognized, please try again."
            )
    except AssertionError:
        assert True

def test_missing_value_imputation(ts_data):
    method = "linear"
    result = tsp.missing_value_imputation(ts_data, "date", numeric_method=method)

    # Test case1: This checks if the given data is of the pandas Dataframe type
    assert isinstance(result, pd.DataFrame), "result should be of type pandas Dataframe"

    # Test case2: This checks if null value is imputed correctly
    assert result.iloc[1, 1] == np.mean([ts_data.iloc[0, 1], ts_data.iloc[2, 1]])
    assert result.iloc[2, 2] == np.mean([ts_data.iloc[1, 2], ts_data.iloc[3, 2]])

def test_exception_on_resampling_rule(ts_data):
    try:
        rule = "8hh"
        method = "prevoius"
        with pytest.raises(ValueError) as exception_info:
            tsp.resampling(ts_data, "date", rule=rule, fill_method=method)
            assert exception_info.match(
                "ValueError: Invalid frequency: 8hh"
            )
    except AssertionError:
        assert True

def test_exception_on_resampling_fill_method(ts_data):
    try:
        n_samples = 12
        method = "prevoius"
        with pytest.raises(Exception) as exception_info:
            tsp.resampling(ts_data, "date", rule=rule, fill_method=method)
            assert exception_info.match(
                "Exception: fill_method not recognized, please try again."
            )
    except AssertionError:
        assert True

def test_resampling(ts_data):
    method = "linear"
    result = tsp.missing_value_imputation(ts_data, "Date", numeric_method=method)

    # Test case1: This checks if the given data is of the pandas Dataframe type
    assert isinstance(result, pd.DataFrame), "result should be of type pandas Dataframe"

    # Test case2: This checks if null value is imputed correctly
    assert result.iloc[1, 1] == np.mean([ts_data.iloc[0, 1], ts_data.iloc[2, 1]])
    assert result.iloc[2, 2] == np.mean([ts_data.iloc[1, 2], ts_data.iloc[3, 2]])

def test_resampling_prev(ts_data):
    method = "previous"
    result = tsp.resampling(ts_data, "date", rule="4H", fill_method=method)
    result["day"] = result["date"].dt.date
    final_result = result.drop_duplicates(subset=result.columns.difference(["date"]))
    assert len(ts_data) == len(final_result)

def test_exception_on_min_max(ts_data):
    try:
        with pytest.raises(Exception) as exception_info:
            tsp.min_max_normalization(ts_data, 1, 0)
            assert exception_info.match(
                "new_max must be greater than new_min. Please adjust and try again."
            )
    except AssertionError:
        assert True

def test_constant_cols_on_min_max(ts_data):
    d = ts_data.copy()
    d["constant"] = 0
    result = tsp.min_max_normalization(d, 0, 1)
    assert sum(result["constant"]) == 0

def test_exception_on_min_max(ts_data):
    d = ts_data.copy()
    d.loc[0, "date"] = np.nan
    result = tsp.index_normalization(d, "date", "1-1-2001", "1-1-2002", "%d-%m-%Y")
    assert len(d) == len(result)
    assert len(d[d["date"].isna()]) == len(result[result["date"].isna()])
