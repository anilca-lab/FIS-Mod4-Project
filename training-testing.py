#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019
The following is a part of the FIS Mod4 Project
The project aims to examine the relationship between stop-question-frisk
and policy effectiveness using data from the NYPD.
This is the code to train and test different models.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("talk")
sns.set_style("white")
df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/df.csv')
# Construct X and y matrices for model fitting
feats = ['stops', 'crimes', 'population', \
         'year','policy', 'pct', \
         'stoprate', 'crimerate', 'stop_arrestrate', \
         'log_stoprate', 'log_crimerate', 'log_population']
X = df[feats]
y = df[['nonstop_arrests','nonstop_arrestrate', 'log_nonstop_arrestrate']]
# Split the data into test and training samples--stratify by year
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = X.year, \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
# Model 1: Absolute values - basic - regress non-stop arrests on stops
lr1 = sm.OLS(y_train[['nonstop_arrests']], sm.add_constant(X_train[['stops']]), hasconst=True)
rslt1 = lr1.fit()
print('Model 1: Absolute values - regress non-stop arrests on stops')
print(rslt1.summary())
# Model 2: Absolute values - regress non-stop arrests on stops and crime
lr2 = sm.OLS(y_train[['nonstop_arrests']], sm.add_constant(X_train[['stops','crimes']]), hasconst=True)
rslt2 = lr2.fit()
print('Model 2: Absolute values - regress non-stop arrests on stops and crime')
print(rslt2.summary())
# Model 3: Absolute values - regress non-stop arrests on stops, crime, and population
lr3 = sm.OLS(y_train[['nonstop_arrests']], sm.add_constant(X_train[['stops','crimes','population']]), hasconst=True)
rslt3 = lr3.fit()
print('Model 3: Absolute values - regress non-stop arrests on stops, crime, population')
print(rslt3.summary())
# Model 4: Switch to rates - regress non-stop arrest rate on stop rate and crime rate
lr4 = sm.OLS(y_train[['nonstop_arrestrate']], sm.add_constant(X_train[['stoprate','crimerate']]), hasconst=True) 
rslt4 = lr4.fit()
print('Model 4: Rates - regress non-stop arrest rate on stop rate and crime rate')
print(rslt4.summary())
# Model 5: Use log transformation on model 4
lr5 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate']]), hasconst=True) 
rslt5 = lr5.fit()
print('Model 5: Log transformation on model 4')
print(rslt5.summary())
# Model 6: Model 5 with log population
lr6 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population']]), hasconst=True) 
rslt6 = lr6.fit()
print('Model 6: Model 5 with log population')
print(rslt6.summary())
# Model 7: Model 5 with log population and linear time trend
lr7 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population','year']]), hasconst=True) 
rslt7 = lr7.fit()
print('Model 7: Model 5 with log population and linear time trend')
print(rslt7.summary())
# Model 8: Model 5 with log population, linear time trend, and policy change variable
lr8 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population','year','policy']]), hasconst=True) 
rslt8 = lr8.fit()
print('Model 8: Model 5 with log population, linear time trend, and policy change')
print(rslt8.summary())
# Model 9: Model 5 with log population, linear time trend, policy change variable, and interactions
poly = PolynomialFeatures(degree = 1)
X_train_poly = poly.fit_transform(X_train[['log_stoprate','log_crimerate','log_population','year','policy']])
X_train_poly = pd.DataFrame(X_train_poly, columns = poly.get_feature_names())
lr9 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(), X_train_poly, hasconst=True) 
rslt9 = lr9.fit()
print('Model 9: Model 5 with log population, linear time trend, policy change variable, and interactions')
print(rslt9.summary())
# Test model 9 for multicollinearity
feats9 = feats[3:5] + feats[6:8] + ['stops_policy_inter', 'sqf_arrests_policy_inter'] 
vif = [variance_inflation_factor(x, i) for i in range(x.shape[1])]
list(zip(feats9, vif))
