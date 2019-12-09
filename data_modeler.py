from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_dataframe(datafile='data/full_df.csv', outfile='data/df.csv'):
    """load dataframe from file"""
    data = pd.read_csv(datafile)
    data = engineer_features(data)
    data.to_csv(outfile, index=False)
    return data

def engineer_features(data):
    """add features to dataframe"""
    data['policy'] = (data.year < 2013).mul(1)
    data['nonstop_arrests'] = data.arrests - data.stop_arrests
    data['crimerate'] = data.crimes / data.population * 1000
    data['nonstop_arrestrate'] = data.nonstop_arrests / data.population * 1000
    data['stoprate'] = data.stops / data.population * 1000
    data['stop_arrestrate'] = data.stop_arrests / data.population * 1000
    data['arrestrate'] = data.arrests / data.population * 1000
    data['normal_year'] = data.year - 2005
    # Two of the precincts (22 in particular) have outlier crime rates
    # (because they have low residential population).
    # drop the outlier precincts, Central Park and Midtown South.
    data = data[~data.pct.isin([22, 14])]
    # the data is skewed. Generate log columns
    log_cols = ['crimerate', 'nonstop_arrestrate', 'stoprate', 'stop_arrestrate', 'arrestrate',
                'nonstop_arrests', 'arrests', 'population', 'stops', 'stop_arrests', 'crimes']
    data[[f'log_{col}' for col in log_cols]] = data[log_cols].apply(np.log).copy()
    return data

def load_split(X, y, **kwargs):
    """basic wrapper for train_test_split"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, **kwargs)
    return {'X_train' : X_train, 'X_test' : X_test, 'y_train' : y_train, 'y_test' : y_test }

def run_ols_no_split(data, x_vars, y_var):
    """run OLS regression with split already done"""
    if not isinstance(x_vars, list):
        x_vars = [x_vars]
    y = data[y_var]
    X = data[x_vars]
    train = X.join(y)
    formula = f'{y_var} ~ {"+".join(x_vars)}'
    lr = ols(formula=formula, data=train)
    return lr.fit()

def run_ols(data, x_vars, y_var):
    """Run OLS regression on data"""
    if not isinstance(x_vars, list):
        x_vars = [x_vars]
    y = data[y_var]
    X = data[x_vars]
    split = load_split(X, y, test_size = 0.2)
    formula = f'{y_var} ~ {"+".join(x_vars)}'
    train = split['X_train'].join(split['y_train'])
    lr = ols(formula=formula, data=train)
    rslt = lr.fit()
    return {'result' : rslt,
            'data' : split }
