from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split

def load_split(X, y, **kwargs):
    """basic wrapper for train_test_split"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, kwargs)
    return {'X_train' : X_train, 'X_test' : X_test, 'y_train' : y_train, 'y_test' : y_test }

def run_ols(data, x_vars, y_var):
    """Run OLS regression on data"""
    y = data[y_var]
    X = data[x_vars]
    formula = f'{y_var} ~ {"+".join(x_vars)}'
    split = load_split(X, y, test_size = 0.2)
    train = split['X_train'].join(split['y_train'])
    lr = ols(formula=formula, data=train)
    rslt = lr.fit()
    return {'result' : rslt,
            'data' : split }
