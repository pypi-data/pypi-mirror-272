import numpy as np 
import pandas as pd
from distfit import distfit
import matplotlib.pyplot as plt
import scipy.stats as stats
import statistics
from collections import Counter
import warnings

continuous_distributions = [
    'norm', 
    'expon', 
    'gamma', 
    'beta', 
    'uniform', 
    'dweibull', 
    'pareto', 
    't', 
    'lognorm'
    ]
discrete_distributions = [
    'poisson', 
    'binom', 
    'geom'
    ]

def _calculate_params(col, distribution='norm'):
    """
    Returns parameter estimates for a single column as a list
    """
    # lowercase text for good measure
    distribution = distribution.lower()
    # access distribution scipy object
    if distribution not in continuous_distributions + discrete_distributions:
        raise ValueError("Distribution input not valid.")
    dist = getattr(stats, distribution)
    if distribution in continuous_distributions:
        return list(dist.fit(col))
    if distribution == 'geom': # for some reason, fitting for geometric distribution works better with no bounds
        res = stats.fit(dist=dist, data=col)
        return list(res.params)
    if distribution == 'poisson' : n = 2
    elif distribution == 'binom' : n = 3
    min_bound = min(np.min(col)*-1.5, 0)
    max_bound = max(np.max(col)*1.5, np.max(col)*-1.5) # multiplying by 1.5 is arbitrary, just need a large enough bounds to capture data
    bounds = [(min_bound, max_bound)] * n 
    res = stats.fit(dist=dist, data=col, bounds=bounds)
    return list(res.params)

def _calculate_pdf(data, distribution='norm'):
    """
    Returns probability density function or probability mass function values for each column.
    For continuous distributions only.
    """
    # dataframe to add pdf values to
    df = pd.DataFrame()
    # access distribution scipy object
    dist = getattr(stats, distribution.lower())
    # calculate pdf values for each column if dataframe passed in
    if isinstance(data, pd.DataFrame):
        for col in data.columns.values:
            if pd.api.types.is_numeric_dtype(data[col]) is False:
                raise ValueError(f"Column {col} must be numeric. Please cast as dtype float or remove from input data.")
            params = _calculate_params(data[col], distribution)
            x = np.linspace(start=np.min(data[col]), stop=np.max(data[col]))
            df[f'{col}_linspace'] = x
            df[f'{col}_pdf'] = dist.pdf(x, *params)
    elif isinstance(data, (pd.Series, list, np.ndarray)):
        if pd.api.types.is_numeric_dtype(data) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        params = _calculate_params(data, distribution)
        x = np.linspace(start=np.min(data), stop=np.max(data))
        df['linspace'] = x
        df['pdf'] = dist.pdf(x, *params)
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")
    return df

def _calculate_pmf(data, distribution):
    """
    Returns probability mass function values for each column.
    For discrete distributions only.
    """
    # dataframe to add pdf values to
    df = pd.DataFrame()
    # access distribution scipy object
    dist = getattr(stats, distribution.lower())
    # calculate pmf values for each column if dataframe passed in
    if isinstance(data, pd.DataFrame):
        for col in data.columns.values:
            if pd.api.types.is_numeric_dtype(data[col]) is False:
                raise ValueError(f"Column {col} must be numeric. Please cast as dtype float or remove from input data.")
            params = _calculate_params(data[col], distribution)
            x = list(range(int(np.min(data[col])), int(np.max(data[col])) + 1))
            original = pd.DataFrame({f'{col}_data':data[col]})
            new = pd.DataFrame({f'{col}_values':x, f'{col}_pmf':dist.pmf(x, *params)})
            df = pd.concat([df, original, new], axis=1)
    elif isinstance(data, (pd.Series, list, np.ndarray)):
        if pd.api.types.is_numeric_dtype(data) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        params = _calculate_params(data, distribution)
        x = list(range(int(np.min(data)), int(np.max(data)) + 1))
        df['values'] = x
        df['pmf'] = dist.pmf(x, *params)
        df = pd.concat([df, data], axis=1)
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")
    return df

def _calculate_quantiles(data, distribution='norm'):
    """
    Returns theoretical quantiles for each column
    For continuous distributions only.
    """
    # lowercase text for good measure
    distribution = distribution.lower()
    # access distribution scipy object
    if distribution not in continuous_distributions:
        raise ValueError("A valid continuous distribution must be inputted.")
    dist = getattr(stats, distribution)
    # calculate quantiles for each column if dataframe passed in
    if isinstance(data, pd.DataFrame):
        # dataframe to add quantiles to
        df = data.copy()
        for col in data.columns.values:
            if pd.api.types.is_numeric_dtype(data[col]) is False:
                raise ValueError(f"Column {col} must be numeric. Please cast as dtype float or remove from input data.")
            params = _calculate_params(data[col], distribution)
            df[f'{col}_pct_rank'] = df[col].rank(pct=True)
            df[f'{col}_theoretical_quant'] = df[f'{col}_pct_rank'].apply(lambda x: dist.ppf(x, *params))
            df = df.drop(columns=[f'{col}_pct_rank']) # drop % rank column
    elif isinstance(data, (pd.Series, list, np.ndarray)):
        df = pd.DataFrame()
        if pd.api.types.is_numeric_dtype(data) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        df['data'] = data
        params = _calculate_params(data, distribution)
        df['pct_rank'] = df['data'].rank(pct=True)
        df['theoretical_quant'] = df['pct_rank'].apply(lambda x: dist.ppf(x, *params))
        df = df.drop(columns=['pct_rank']) # drop % rank column
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")
    return df

def _get_dimensions(n):
    """
    Gets optimal subplots dimensions for _generate_plots.
    """
    if n == 1:
        return 1, 1
    def _is_prime(n):
        for i in range(2, int(n/2)+1):
            if (n % i) == 0:
                return False
        return True
    def _get_dimensions(n):
        if _is_prime(n) == True:
            n += 1
        divisors = []
        currentDiv = 1
        for currentDiv in range(n):
            if n % float(currentDiv + 1) == 0:
                divisors.append(currentDiv+1)
        hIndex = min(range(len(divisors)), key=lambda i: abs(divisors[i]-np.sqrt(n)))
        return divisors, hIndex
    
    divisors, hIndex = _get_dimensions(n)

    # adjust dimensions to prevent long, skinny set of subplots
    if _is_prime(divisors[hIndex+1]) == True:
       divisors, hIndex = _get_dimensions(n+1)
    
    if divisors[hIndex]*divisors[hIndex] == n:
        return divisors[hIndex], divisors[hIndex]
    else:
        wIndex = hIndex + 1
        return divisors[hIndex], divisors[wIndex]
    
def _clean_plots(ax, var_name):
    ax.set_title(var_name)
    ax.set_xlabel('Values')
    ax.set_ylabel('Density')
    ax.spines[['top', 'right']].set_visible(False)

def _generate_plots(data, plot_type, distribution='norm'):
    """
    Generates premade plots.
    """
    # access distribution scipy object
    dist = getattr(stats, distribution.lower())
    # set up arrangement of plots if dataframe is passed in
    if isinstance(data, pd.DataFrame):
        dims = _get_dimensions(len(data.columns.values))
        nrow, ncol, i = 0, 0, 0
        # multiplier for figsize proportional to number of columns, should be at least 3
        n = max(int(len(data.columns) / 3), 3)
        plt.figure(figsize=(dims[1]*n,dims[0]*n))

        # get actual plots
        if plot_type == 'qq':
            for col in data.columns.values:
                ax = f'a{i}'
                ax = plt.subplot2grid(dims, (nrow, ncol), rowspan=1, colspan=1)
                params = _calculate_params(data[col], distribution)
                res = stats.probplot(data[col], dist=dist, sparams=params, plot=ax)
                ax.get_lines()[0].set_markersize(4.0)
                _clean_plots(ax, col)
                ncol += 1
                if ncol == dims[1]:
                    nrow += 1
                    ncol = 0
        else: # histograms
            for col in data.columns.values:
                ax = f'a{i}'
                ax = plt.subplot2grid(dims, (nrow, ncol), rowspan=1, colspan=1)
                # ax.hist(data[col], bins=int(round(len(data)/10,0)), density=True)
                ax.hist(data[col], density=True)
                params = _calculate_params(data[col], distribution)
                if distribution in continuous_distributions:
                    x = np.linspace(np.min(data[col]), np.max(data[col]))
                    ax.plot(x, dist.pdf(x, *params),)
                else: # discrete
                    x = list(range(int(np.min(data[col])), int(np.max(data[col])) + 1))
                    ax.scatter(x, dist.pmf(x, *params), color='red')
                _clean_plots(ax, col)
                ncol += 1
                if ncol == dims[1]:
                    nrow += 1
                    ncol = 0
        plt.tight_layout()
        plt.show()

    elif isinstance(data, (pd.Series, list, np.ndarray)):
        fig, ax = plt.subplots()
        params = _calculate_params(data, distribution)
        if plot_type == 'qq':
            res = stats.probplot(data, dist=dist, sparams=params, plot=ax)
            ax.get_lines()[0].set_markersize(4.0)
            _clean_plots(ax, 'Q-Q plot')
        else:
            ax.hist(data, bins=int(round(len(data)/10,0)), density=True)
            if distribution in continuous_distributions:
                x = np.linspace(np.min(data), np.max(data))
                ax.plot(x, dist.pdf(x, *params),)
            else:
                x = list(range(int(np.min(data)), int(np.max(data)) + 1))
                ax.scatter(x, dist.pmf(x, *params), color='red')
            _clean_plots(ax, 'Histogram')
        plt.show()

def _calculate_frequencies(obs_data, distribution, params):
    """
    Calculates observed and expected frequencies for discrete distributions to calculate chi-squared value.
    For discrete distributions only.
    """
    # observed frequencies
    obs_c = dict(sorted(Counter(obs_data).items()))
    # initialize dataframe
    freqs = {'Value':[], 'Observed':[]}
    for k, v in obs_c.items():
        freqs['Value'].append(k)
        freqs['Observed'].append(v)
    freqs_df = pd.DataFrame(freqs)
    # calculate expected frequencies based on distribution
    expected_values = []
    distribution = distribution.lower() # lowercase text for good measure
    if distribution == 'binom':
        n = int(params[0])
        p = params[1]
        for v in freqs_df['Value'].values:
            expected = freqs_df['Observed'].sum() * getattr(stats, distribution).pmf(k=v, n=n, p=p)
            expected_values.append(expected)
    else:
        for v in freqs_df['Value'].values:
            expected = freqs_df['Observed'].sum() * getattr(stats, distribution).pmf(v, *params)
            expected_values.append(expected)
    freqs_df['Expected'] = expected_values
    # chi squared can't be calculated with any expected values of 0
    freqs_nonzero = freqs_df[freqs_df['Expected'] > 0]
    return freqs_nonzero

def _chi_square(obs, exp, ddof=1):
    """
    Calculates chi-squared value and p-value.
    For discrete distributions only.
    """
    if len(obs) != len(exp):
        raise ValueError()
    x2 = 0
    for i in range(len(obs)): 
        x2 += (obs[i] - exp[i])**2 / exp[i]
    p = 1 - stats.chi2.cdf(x2, len(obs)-1-ddof)
    return x2, p

def visual_normality_testing(data, plot_type='histogram', return_params=False, return_plots=False):
    """
    Computes necessary outputs to produce histograms with normal probability curves or Q-Q plots in Spotfire for each input column. Optionally, this function will return parameter estimates and premade plots.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) to produce visual normality test outputs for. Data must be numeric.
    plot_type : str, required (default='histogram')
        Specify if histograms with probability curve or Q-Q plot is wanted.
    return_params : bool, optional (default=False)
        Indicates if user wants parameter estimates returned.
    return_plots : bool, optional (default=False)
        Indicates if user wants premade plots returned.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe of probability density function values (if plot_type='histogram') or theoretical quantiles (if plot_type='qq') for each input value.
    params : dictionary or list
        Parameter estimates for each column following a normal distribution. Optional, returned when return_params=True
    plots : matplotlib figure
        Premade plots (histograms if plot_type='histogram' and Q-Q plots if plot_type='qq'). Optional, returned when return_plots=True

    Notes on using outputs to create histograms
    -------------------------------------------
    • The histogram y-axis should be showing density or proportion
        • In Spotfire, this looks like aggregating the y-axis to the aggregation '% of Total (Row Count)'
        • In matplotlib, this looks like having the parameter density = True.
    • The histogram x-axis should be the original data column
    • The PDF column of the output table should be plotted as an overlaid line plot.
        • In Spotfire, this can be done using the Lines & Curves property of the histogram, and adding a 'Line from Column Values' using the PDF column values for the y-axis and the linspace values for the x-axis.
    
    Notes on using outputs to create Q-Q plots
    ------------------------------------------
    • The outputs for a Q-Q plot can be visualized with a scatter plot
        • The Q-Q plot y-axis should be the theoretical quantiles
        • The Q-Q plot x-axis should be the observed quantiles, i.e. the original data
    • For comparison, plot an overlaid straight line where y = x.
        • In Spotfire, this can be done using the Lines & Curves property of the histogram, and adding a 'Curve Draw' where the Curve expression is y = x.
    
    Notes on optional outputs
    -------------------------
    • Optional outputs (list or dictionary for parameters, matplotlib figure for plots) will not be compatible with Spotfire outputs.
    • If using this function in a Spotfire data function, set return_params = False and return_plots = False to avoid data type related issues.
    """
    if plot_type == 'histogram':
        df = _calculate_pdf(data)
    elif plot_type == 'qq':
        df = _calculate_quantiles(data)
    else:
        warnings.warn("plot_type not recognized, default 'histogram' used.")
        df = _calculate_pdf(data)

    if return_plots:
        _generate_plots(data, plot_type)

    if return_params:
        if isinstance(data, pd.DataFrame):
            params = {}
            for col in data.columns.values:
                params[col] = _calculate_params(data[col])
        else: # no error message here, is integrated up above
            params = _calculate_params(data)
        return df, params
    return df 

def statistical_normality_testing(data, alpha=0.05):
    """
    Conduct Shapiro-Wilk and Anderson-Darling tests to test data column(s) for normality.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) to conduct normality tests on. Data must be numeric.
    alpha : float, optional (default=0.05)
        Significance level for interpreting test results.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe with test results, p-values, and interpretations.

    Notes
    -----
    • The Shapiro-Wilk test is a test of normality. For more information, go to https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test
    • The Anderson-Darling test tests whether a sample of data has likely come from a particular distribution. In this case, that is a normal distribution.
        For more information, go to https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test 
    """
    def _perform_norm_tests(col, alpha):
        if pd.api.types.is_numeric_dtype(col) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")

        # parameters
        res_dict["Mean"].append(np.mean(col))
        res_dict["StandardDeviation"].append(statistics.stdev(col))

        # Shapiro-Wilk test
        sw_stat, sw_pval = stats.shapiro(col)
        res_dict["ShapiroWilkTestStatistic"].append(sw_stat)
        res_dict["ShapiroWilkTestPValue"].append(sw_pval)
        res_dict["ShapiroWilkAlpha"].append(alpha)
        if sw_pval <= alpha:
            res_dict["ShapiroWilkTestInterpretation"].append("Test indicates the data is NOT normally distributed.")
        else:
            res_dict["ShapiroWilkTestInterpretation"].append("Test indicates the data IS normally distributed.")
            
        # Anderson-Darling test
        res = stats.anderson(col)
        ad_stat = res[0]
        # find appropriate cv based on alpha
        ad_sig_levels = list(res[2])
        if alpha * 100 in ad_sig_levels:
            i = ad_sig_levels.index(alpha * 100)
            ad_cv = res[1][i]
        else: # if alpha not available, use alpha = 0.05
            warnings.warn("alpha value not available in Anderson-Darling significance levels, default 0.05 used.")
            ad_cv = res[1][2]
            alpha = 0.05
        res_dict["ADTestStatistic"].append(ad_stat)
        res_dict["ADTestCV"].append(ad_cv)
        res_dict["ADAlpha"].append(alpha)
        if ad_stat > ad_cv:
            res_dict["ADTestInterpretation"].append("Test indicates the data is NOT normally distributed.")
        else:
            res_dict["ADTestInterpretation"].append("Test indicates the data IS normally distributed.")
    
    # initialize dictionary for dataframe
    res_dict = {
        "ColumnName":[],
        "Mean":[],
        "StandardDeviation":[],
        "ShapiroWilkTestStatistic":[],
        "ShapiroWilkTestPValue":[],
        "ShapiroWilkAlpha":[],
        "ShapiroWilkTestInterpretation":[],
        "ADTestStatistic":[],
        "ADTestCV":[],
        "ADAlpha":[],
        "ADTestInterpretation":[],
    }

    # iterate through columns to produce results if dataframe is passed in
    if isinstance(data, pd.DataFrame):
        input_cols = data.columns.values
        for col in input_cols:
            _perform_norm_tests(data[col], alpha)
            res_dict["ColumnName"].append(col)
        df = pd.DataFrame(res_dict)
    # if one column is passed in
    elif isinstance(data, (pd.Series, np.ndarray, list)):
        _perform_norm_tests(data, alpha)
        res_dict["ColumnName"].append('dummy input') # to be deleted
        df = pd.DataFrame(res_dict)
        df = df.drop(columns=['ColumnName'])
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")
    
    return df

def estimate_population_parameters(data, distributions):
    # """
    # Estimate population parameters for one or more columns given one or more distributions.

    # Parameters
    # ----------
    # data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
    #     The column(s) to estimate population parameters for. Data must be numeric.
    # distributions : str or dict, required
    #     A string or dictionary indicating the distribution or distributions to have parameters estimated for.
    #     Allowed distributions:
    #     • 'norm'
    #     • 'expon'
    #     • 'gamma'
    #     • 'beta'
    #     • 'uniform'
    #     • 'dweibull'
    #     • 'pareto'
    #     • 't'
    #     • 'lognorm'
    #     • 'poisson'
    #     • 'binom'
    #     • 'geom'
    #     For one column only, distributions input should be type str.
    #     Dict inputs should be formatted as {key=column_name:value=distribution}

    # Returns
    # -------
    # params : pandas.DataFrame
    #     Dataframe with distribution and parameter estimates for each column
    # """

    # iterate through columns to produce results if dataframe is passed in
    if isinstance(data, pd.DataFrame):
        input_cols = data.columns.values
        output_dict = {
            "Column Name":[],
            "Distribution":[],
            "Parameters":[]
        }
        for col in input_cols:
            if pd.api.types.is_numeric_dtype(data[col]) is False:
                raise ValueError(f"Column {col} must be numeric. Please cast as dtype float or remove from input data.")
            if isinstance(distributions, str):
                dist_name = distributions
            elif isinstance(distributions, dict) and col in distributions:
                dist_name = distributions[col]
            else:
                raise ValueError("Could not estimate parameters. Either an invalid distribution or no distribution value was passed for this column.")
            
            params_list = _calculate_params(data[col], dist_name)
            params = ', '.join([str(p) for p in params_list])
            output_dict['Column Name'].append(col)
            output_dict['Distribution'].append(dist_name)
            output_dict['Parameters'].append(params)

    elif isinstance(data, (pd.Series, np.ndarray, list)):
        output_dict = {
            "Distribution":[],
            "Parameters":[]
        }
        if pd.api.types.is_numeric_dtype(data) is False:
                raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        if isinstance(distributions, str):
            dist_name = distributions
        else:
            raise ValueError("Could not estimate parameters. Either an invalid distribution or no distribution value was passed for this column.")
        
        params_list = _calculate_params(data, dist_name)
        params = ', '.join([str(p) for p in params_list])
        output_dict['Distribution'].append(dist_name)
        output_dict['Parameters'].append(params)

    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")

    return pd.DataFrame(output_dict)

def visual_distribution_fitting(data, distribution, plot_type='histogram', return_params=False, return_plots=False):
    """
    Computes necessary outputs to produce histograms with probability density curves or Q-Q plots in Spotfire for each input column. Optionally, this function will return parameter estimates and premade plots.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) to produce visual normality test outputs for. Data must be numeric.
    distribution : str, required
        Allowed distributions:
        • 'norm'
        • 'expon'
        • 'gamma'
        • 'beta'
        • 'uniform'
        • 'dweibull'
        • 'pareto'
        • 't'
        • 'lognorm'
        • 'poisson'
        • 'binom'
        • 'geom'
    plot_type : str, required (default='histogram')
        Specify if histograms with probability curve or Q-Q plot is wanted.
    return_params : bool, optional (default=False)
        Indicates if user wants parameter estimates returned.
    return_plots : bool, optional (default=False)
        Indicates if user wants premade plots returned.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe of probability density/mass function values (if plot_type='histogram') or theoretical quantiles (if plot_type='qq') for each input value.
    params : dictionary
        Parameter estimates for each column following a normal distribution. Optional, returned when return_params=True
    plots : matplotlib figure
        Premade plots (histograms if plot_type='histogram' and Q-Q plots if plot_type='qq'). Optional, returned when return_plots=True

    Notes
    -----
    • Q-Q plots are not available for discrete distributions (poisson, geometric, binomial).

    Notes on using outputs to create histograms
    -------------------------------------------
    • The histogram y-axis should be showing density or proportion
        • In Spotfire, this looks like aggregating the y-axis to the aggregation '% of Total (Row Count)'
        • In matplotlib, this looks like having the parameter density = True.
    • The histogram x-axis should be the original data column
    • The PDF column of the output table should be plotted as an overlaid line plot.
        • In Spotfire, this can be done using the Lines & Curves property of the histogram, and adding a 'Line from Column Values' using the PDF column values for the y-axis and the linspace values for the x-axis.
    
    Notes on using outputs to create Q-Q plots
    ------------------------------------------
    • The outputs for a Q-Q plot can be visualized with a scatter plot
        • The Q-Q plot y-axis should be the theoretical quantiles
        • The Q-Q plot x-axis should be the observed quantiles, i.e. the original data
    • For comparison, plot an overlaid straight line where y = x.
        • In Spotfire, this can be done using the Lines & Curves property of the histogram, and adding a 'Curve Draw' where the Curve expression is y = x.
    
    Notes on optional outputs
    -------------------------
    • Optional outputs (list or dictionary for parameters, matplotlib figure for plots) will not be compatible with Spotfire outputs.
    • If using this function in a Spotfire data function, set return_params = False and return_plots = False to avoid data type related issues.
    """
    if distribution.lower() in discrete_distributions and plot_type != 'histogram':
        warnings.warn("plot_type for discrete distributions must be 'histogram', default 'histogram' used.")
        plot_type = 'histogram'

    if plot_type == 'histogram':
        df = pd.DataFrame()
        if distribution in discrete_distributions:
            df = _calculate_pmf(data, distribution)
        else:
            df = _calculate_pdf(data, distribution)
    elif plot_type == 'qq':
        df = _calculate_quantiles(data, distribution)
    else:
        raise ValueError("plot_type input not recognized.")

    if return_plots:
        _generate_plots(data, plot_type, distribution)

    if return_params:
        if isinstance(data, pd.DataFrame):
            params = {}
            for col in data.columns.values:
                params[col] = _calculate_params(data[col], distribution)
        else: # no error message here, is integrated up above
            params = _calculate_params(data, distribution)
        return df, params
    return df   

def statistical_distribution_fitting(data, dist_params, alpha=0.05):
    """
    Conduct Kolmogorov-Smirnov or chi-squared tests to test data columns for goodness of fit against a theoretical distribution.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) to conduct goodness of fit tests on. Data must be numeric.
    dist_params : pandas.DataFrame, required
        A dataframe matching the output of estimate_population_parameters, containing the selected distribution 
        and parameters (or parameter estimates) for each column.
        Allowed distributions:
        • 'norm'
        • 'expon'
        • 'gamma'
        • 'beta'
        • 'uniform'
        • 'dweibull'
        • 'pareto'
        • 't'
        • 'lognorm'
        • 'poisson'
        • 'binom'
        • 'geom'
    alpha : float, optional (default=0.05)
        Significance level for interpreting test results.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe with test results, p-values, and interpretations.

    Notes
    -----
    • The Kolmogorov-Smirnov test tests for equality of continuous probability distributions to test whether a sample likely came from a particular distribution.
        For more information, go to https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test 
    • The Chi-Squared test measures whether two categorical variables are independent of each other.
        In this case, the two categorical variables are the observed and expected frequencies of a discrete distribution.
        To test if the sample has likely come from a particular distribution, we are looking to find out if the are not independent of each other.
        Please note that chi-squared tests work best on larger datasets.
        For more information, go to https://en.wikipedia.org/wiki/Chi-squared_test
    """
    def _perform_stat_test(col, distribution, params):
        if pd.api.types.is_numeric_dtype(col) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        output_dict["Distribution"].append(distribution)
        
        # Kolmogorov-Smirnov test
        if distribution in continuous_distributions:
            ks_stat, ks_pval = stats.kstest(col, distribution, params)
            output_dict["Test"].append("KS Test")
            output_dict["Test Statistic"].append(ks_stat)
            output_dict["Test p-value"].append(ks_pval)
            if ks_pval <= alpha:
                output_dict["Test Interpretation"].append("Test indicates the data does NOT fit this distribution with the given parameters.")
            else:
                output_dict["Test Interpretation"].append("Test indicates the data DOES fit this distribution with the given parameters.")
        # Chi-squared test
        elif distribution in discrete_distributions:
            # calculate expected and observed frequencies first
            freqs = _calculate_frequencies(col, distribution, params)
            observed_freqs = freqs['Observed'].values
            expected_freqs = freqs['Expected'].values
            ddof = 1 # delta degrees of freedom
            if distribution == 'binom':
                ddof = 2
            x2, p = _chi_square(observed_freqs, expected_freqs, ddof)
            output_dict["Test"].append("Chi-squared Test")
            output_dict["Test Statistic"].append(x2)
            output_dict["Test p-value"].append(p)
            if p <= alpha:
                output_dict["Test Interpretation"].append("Test indicates the data does NOT fit this distribution with the given parameters.")
            else:
                output_dict["Test Interpretation"].append("Test indicates the data DOES fit this distribution with the given parameters.")
        else:
            raise ValueError("Distribution input not valid.")
    # convert parameters back to a list
    dist_params_copy = dist_params.copy() # as to not alter original input
    dist_params_copy['Parameters'] = dist_params_copy['Parameters'].apply(lambda x: x.split(', ')).apply(lambda x: [float(i) for i in x])
    
    # initialize dictionary for dataframe
    output_dict = {
        "Column Name":[],
        "Distribution":[],
        "Test":[],
        "Test Statistic":[],
        "Test p-value":[],
        "Test Interpretation":[]
    }

    # iterate through columns to produce results if dataframe is passed in
    if isinstance(data, pd.DataFrame):
        input_cols = data.columns.values
        for col in input_cols:
            dist = dist_params_copy[dist_params_copy['Column Name'] == col]['Distribution'].values[0]
            params = dist_params_copy[dist_params_copy['Column Name'] == col]['Parameters'].values[0]
            _perform_stat_test(data[col], dist, params)
            output_dict['Column Name'].append(col)
        df = pd.DataFrame(output_dict)
    # if one column is passed in
    elif isinstance(data, (pd.Series, np.ndarray, list)):
        dist = dist_params_copy['Distribution'][0]
        params = dist_params_copy['Parameters'][0]
        _perform_stat_test(data, dist, params)
        output_dict['Column Name'].append('dummy input') # to be deleted
        df = pd.DataFrame(output_dict)
        df = df.drop(columns=['Column Name'])
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")
    return df

def predict_best_distribution(data):
    """
    Predicts the best fit distribution and parameters for a set of columns.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) to conduct goodness of fit tests on. Data must be numeric.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe with best fit distribution, RSS value, and parameter estimates.

    Notes
    -----
    • Residual sum of squares (RSS) is the goodness of fit measure used to compare input data to a variety of theoretical distributions.
        For more information on the RSS measure, go to https://en.wikipedia.org/wiki/Residual_sum_of_squares
    """
    def _perform_distfit(col):
        if pd.api.types.is_numeric_dtype(col) is False:
            raise ValueError(f"Column must be numeric. Please cast as dtype float or remove from input data.")
        
        dist = distfit(distr=continuous_distributions)
        res = dist.fit_transform(col.values, verbose=0)
        summary = dist.summary
        best = summary.loc[0]
        res_dict['Distribution'].append(best['name'])
        res_dict['RSS'].append(best['score'])
        res_dict['Loc'].append(best['loc'])
        res_dict['Scale'].append(best['scale'])
        res_dict['Shape Parameters'].append(', '.join([str(p) for p in best['arg']]))
        
    # initialize dictionary for dataframe
    res_dict = {
        "Column Name":[],
        "Distribution":[],
        "RSS":[],
        "Loc":[],
        "Scale":[],
        "Shape Parameters":[]
    }

    # iterate through columns to produce results if dataframe is passed in
    if isinstance(data, pd.DataFrame):
        input_cols = data.columns.values
        for col in input_cols:
            _perform_distfit(data[col])
            res_dict["Column Name"].append(col)
        df = pd.DataFrame(res_dict)
    # if one column is passed in
    elif isinstance(data, (pd.Series, np.ndarray, list)):
        _perform_distfit(data)
        res_dict["Column Name"].append('dummy input') # to be deleted
        df = pd.DataFrame(res_dict)
        df = df.drop(columns=['Column Name'])
    else:
        raise ValueError("Invalid input data type. Input data should be pd.DataFrame, pd.Series, np.ndarray, or a list.")

    return df

def predict_proba(data, distribution, params):
    """
    Compute probabilities of occurrence for a given distribution and set of parameters for a column or array of data.

    Parameters
    ----------
    data : array-like (pd.Series, np.ndarray, list), required
        Column or array of values to predict probabilities for. Data must be numeric and unimodal.
    distribution : str, required
        Distribution to predict probabilities within.
        Allowed distributions:
        • 'norm'
        • 'expon'
        • 'gamma'
        • 'beta'
        • 'uniform'
        • 'dweibull'
        • 'pareto'
        • 't'
        • 'lognorm'
        • 'poisson'
        • 'binom'
        • 'geom'
    params : str, required
        String of parameters or parameter estimates for the given distribution. Should be ordered as shape parameters, loc, scale. Delimiter should be a comma followed by a space, i.e. ", "

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe of input data and respective probabilities.

    Notes
    -----
    • Probabilities are calculated using the probability density function for continuous variables, and probability mass function for discrete variables.
    """
    # store results
    res_dict = {'Actual Value':[], 'Predicted Probability':[]}

    # convert parameters to list type
    params_list = [float(x) for x in params.split(', ')]
    # get scipy stats object from dictionary and check inputs
    if distribution.lower() in continuous_distributions:
        dist = getattr(stats, distribution.lower())
        for i in range(len(data)):
            proba = dist.pdf(data[i], *params_list) 
            res_dict['Actual Value'].append(data[i])
            res_dict['Predicted Probability'].append(proba)
    elif distribution.lower() in discrete_distributions:
        dist = getattr(stats, distribution.lower())
        for i in range(len(data)):
            proba = dist.pmf(data[i], *params_list) 
            res_dict['Actual Value'].append(data[i])
            res_dict['Predicted Probability'].append(proba)
    else:
        raise ValueError("Invalid input for distribution.")

    df = pd.DataFrame(res_dict)
    return df
