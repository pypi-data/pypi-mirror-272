def SignalGenerator(n_samples = 100, freq1 = 5, freq2 = 7, dc = 10, freq_sign = -1, addition=True):
    """Generates a signal based on user input

    Input:
        n_samples (int, optional): No. of samples. Defaults to 100.
        freq1 (int, optional): Component1 frequency. Defaults to 5.
        freq2 (int, optional): Component2 frequency. Defaults to 7.
        dc (int, optional): Constant component. Defaults to 10.
        freq_sign (int, optional): Sign given to 1st component. Defaults to -1.
        addition (bool, optional): Add or multiply components. Defaults to True.

    Returns:
        DataFrame: DataFrame contains (index, trend, seasonal, resid)
    """
    import numpy as np
    import pandas as pd
    x = np.arange(n_samples) # the points on the x axis for plotting

    # constructing the signal
    y1 = 2*np.cos(2*np.pi*freq1 * (x/n_samples)  + freq_sign* np.pi/2)
    y2 = 3*np.cos(-2*np.pi*freq2 * (x/n_samples) )
    dc = np.ones_like(x)*dc
    if addition:
        combined = pd.DataFrame({'data':np.array(y1+y2+dc)})
    else:
        combined = pd.DataFrame({'data':np.array(y1*y2+dc)})
    return y1, y2, combined
def DataPrep(ts, index, data_col, ts_delta):
    """Data prep function

    Input:
        ts (Data Frame):
            A data frame where a column is the timestamp or index
            and the other column is readings of the variable at corresponding timestamps.
            The number of columns can be one (values only) or two (timestamp and value).
            provided, the function will assume it is a value column and it will create an index. The 
            assumption here is that the provided time series is equally spaced.
        index(str, int)[Optional]: 
            if string, it is interpreted as the name of the column. 
            If numeric it is considered the index of the timestamp column; value of -1
            indicates that there is no index column and the function will create the index column, default is 0.
        data_col(str, int)[Optional]: 
            Data column name, index, default is 1
        ts_delta (str)[Optional]:
            Sets the frequency in cases when timestamp is not provided.

    Returns:
        ts: Prepared dataframe
    """
    import pandas as pd
    from datetime import datetime
    ts = ts.copy()
    # assert number of columns is <3
    ncols = len(ts.columns) 
    assert ncols <3, 'Max. no. of columns must be 2'
    assert index != data_col, 'Index and data column should not be the same'
    if isinstance(index, int):
        assert index in [-1,0,1], 'Index should be -1, 0 or 1'
# check if index is provided in the data
    if ncols == 1:
        index = -1
        data_col = 0
    if index == -1:
        if (isinstance(data_col, int)):
            data_col = ts.columns[data_col]
        new_index = pd.date_range(datetime.now(), periods=len(ts), freq=ts_delta)
        ts.insert(loc=0, column = 'new_index', value = new_index)
        ts.set_index('new_index', inplace=True)
        ts.index = pd.to_datetime(ts.index)
        ts = ts.loc[:, data_col]
    if (index ==1 or index ==0):
        ts.set_index(ts.columns[index], inplace=True)
        ts.index = pd.to_datetime(ts.index)
    elif(isinstance(index, str)):
        ts.set_index(index, inplace=True)
        ts.index = pd.to_datetime(ts.index)
    return ts

def ConvDecompose(ts, index=0, data_col = 1, model = 'additive', ts_delta = 'D'):
    """ Decomposes Time Series
    
    Input:
        ts (Data Frame): 
            A data frame where a column is the timestamp or index
            and the other column is readings of variables at corresponding timestamps. 
            The number of columns can be one (values only) or two (timestamp and value).
            Maximum number of columns should be 2. The values have to be numeric.
        index(str, int)[Optional]:
            if string it is interpreted as the name of the column. 
            If numeric it is considered the index of the timestamp column; value of -1
            indicates that there is no index column and the function will create the index column, default is 0.
        data_col(str, int)[Optional]:
            Data column name, index, default is 1
        model(str)[Optional]:
            The decomposing model ['additiv', 'multiplicative'] default is ''additive'
        ts_delta (str): 
            Sets the timestamp frequency.
        
    Returns:
        timestamps: list of datetime index
        trend: One column array shows the decomposed trend
        seasonality: One column array shows seasonality
        resid: One column array shows the residuals
    """
    import pandas as pd
    from statsmodels.tsa.seasonal import seasonal_decompose
    from dateutil.parser import parse
    
    
    ts = DataPrep(ts, index, data_col, ts_delta)
    
    #decomposing
    results = seasonal_decompose(ts, model = model)
    timestamps = ts.index
    seasonality = results.seasonal
    trend = results.trend
    resid = results.resid
    final_df = pd.concat([trend, seasonality, resid], axis=1)
    final_df.reset_index(inplace=True)
    return final_df
    
def FftDecompose(ts, index=0, data_col = 1, ts_delta = 'D'):
    """ Decomposes Time Series

    Input:
        ts (Data Frame):
            A data frame where a column is the timestamp or index
            and the other column is readings of the variable at corresponding timestamps. 
            The number of columns can be one (values only) or two (timestamp and value).
            Maximum number of columns should be 2. The values have to be numeric. If one column is
            provided, the function will assume it is a value column and it will create an index. The 
            assumption here is that the provided time series is equally spaced.
        index(str, int)[Optional]:
            if string, it is interpreted as the name of the column. 
            If numeric it is considered the index of the timestamp column; value of -1
            indicates that there is no index column and the function will create the index column, default is 0.
        data_col(str, int) [Optional]:
            Data column name, index, default is 1
        ts_delta (str) [Optional]:
            Sets the frequency in cases when timestamp is not provided.
    
    Returns:
        fr_amplitude: Magnitude of the frequency component at the corresponding frequency using Discrete Fourier Transformation
        fr_phase: Phase of the frequency component at the corresponding frequency using Discrete Fourier Transformation in Radian
    """
    import numpy as np
    from numpy.fft import rfft
    import pandas as pd
    ts = DataPrep(ts, index, data_col, ts_delta)

    # DFT decomposing
    fr_signal = rfft(ts)
    return fr_signal

def fftInverse(fr_signal):
    from numpy.fft import irfft
    """ performs inverse fourier transform
    Input:
        fr_signal (Data Frame): Magnitude of the frequency component at the corresponding frequency using Discrete Fourier Transformation
    Returns:
        signal: recomposed signal using inverse fourier transfer
    """
    signal = irfft(fr_signal)
    return signal