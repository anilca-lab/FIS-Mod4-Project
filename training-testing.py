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

# Function to extract and update poly feat names
def extract_poly_feat_names(poly, df_feats):
    poly_feat_names = poly.get_feature_names()
    updated_poly_feat_names = []
    for name in poly_feat_names:
        updated_name = name
        for i in range(len(df_feats)):
            if f'x{i}' in updated_name: 
                updated_name = updated_name.replace(f'x{i}', df_feats[i])
        updated_poly_feat_names.append(updated_name)
    return updated_poly_feat_names

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
print('\nModel 1: Absolute values - regress non-stop arrests on stops')
print(rslt1.summary())
# Model 2: Absolute values - regress non-stop arrests on stops and crime
lr2 = sm.OLS(y_train[['nonstop_arrests']], sm.add_constant(X_train[['stops','crimes']]), hasconst=True)
rslt2 = lr2.fit()
print('\nModel 2: Absolute values - regress non-stop arrests on stops and crime')
print(rslt2.summary())
# Model 3: Absolute values - regress non-stop arrests on stops, crime, and population
lr3 = sm.OLS(y_train[['nonstop_arrests']], sm.add_constant(X_train[['stops','crimes','population']]), hasconst=True)
rslt3 = lr3.fit()
print('\nModel 3: Absolute values - regress non-stop arrests on stops, crime, population')
print(rslt3.summary())
# Model 4: Switch to rates - regress non-stop arrest rate on stop rate and crime rate
lr4 = sm.OLS(y_train[['nonstop_arrestrate']], sm.add_constant(X_train[['stoprate','crimerate']]), hasconst=True) 
rslt4 = lr4.fit()
print('\nModel 4: Rates - regress non-stop arrest rate on stop rate and crime rate')
print(rslt4.summary())
# Model 5: Use log transformation on model 4
lr5 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate']]), hasconst=True) 
rslt5 = lr5.fit()
print('\nModel 5: Log transformation on model 4')
print(rslt5.summary())
# Model 6: Model 5 with log population
lr6 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population']]), hasconst=True) 
rslt6 = lr6.fit()
print('\nModel 6: Model 5 with log population')
print(rslt6.summary())
# Model 7: Model 5 with log population and linear time trend
lr7 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population','year']]), hasconst=True) 
rslt7 = lr7.fit()
print('\nModel 7: Model 5 with log population and linear time trend')
print(rslt7.summary())
# Model 8: Model 5 with log population, linear time trend, and policy change variable
lr8 = sm.OLS(y_train[['log_nonstop_arrestrate']], sm.add_constant(X_train[['log_stoprate','log_crimerate','log_population','year','policy']]), hasconst=True) 
rslt8 = lr8.fit()
print('\nModel 8: Model 5 with log population, linear time trend, and policy change')
print(rslt8.summary())
# Model 9: Model 5 with log population, linear time trend, policy change variable, and interactions
poly = PolynomialFeatures(interaction_only = True, include_bias = False)
X_train_poly = poly.fit_transform(X_train[['log_stoprate','log_crimerate','log_population','year','policy']])
X_train_poly_feat_names = extract_poly_feat_names(poly, ['log_stoprate','log_crimerate','log_population','year','policy'])
X_train_poly = pd.DataFrame(X_train_poly, columns = X_train_poly_feat_names)
lr9 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(X_train_poly), hasconst=True) 
rslt9 = lr9.fit()
print('\nModel 9: Model 5 with log population, linear time trend, policy change variable, and interactions')
print(rslt9.summary())
# Test model 9 for multicollinearity
vif = [variance_inflation_factor(X_train_poly.values, i) for i in range(X_train_poly.values.shape[1])]
print('\nModel 9: Multicollinearity test')
print(list(zip(X_train_poly_feat_names, vif)))
# Model 10: Model 9 with year interactions dropped
x = X_train_poly.drop(['log_stoprate year', 'log_crimerate year', 'log_population year', 'year policy'], axis = 1)
lr10 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(x), hasconst=True) 
rslt10 = lr10.fit()
print('\nModel 10: Model 9 with year interactions dropped')
print(rslt10.summary())
# Test model 10 for multicollinearity
vif = [variance_inflation_factor(x.values, i) for i in range(x.values.shape[1])]
print('\nModel 10: Multicollinearity test')
print(list(zip(x.columns, vif)))
# Model 11: Model 9 with year interactions and population dropped
x = X_train_poly.drop(['log_stoprate year', 'log_crimerate year', 'log_population year', 'year policy', 'log_population', \
                       'log_stoprate log_population', 'log_crimerate log_population', 'log_population policy'], axis = 1)
lr11 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(x), hasconst=True) 
rslt11 = lr11.fit()
print('\nModel 11: Model 9 with year interactions and population dropped')
print(rslt11.summary())
# Test model 11 for multicollinearity
vif = [variance_inflation_factor(x.values, i) for i in range(x.values.shape[1])]
print('\nModel 11: Multicollinearity test')
print(list(zip(x.columns, vif)))
# Model 12: Model 9 with year interactions and crime dropped
x = X_train_poly.drop(['log_stoprate year', 'log_crimerate year', 'log_population year', 'year policy', 'log_crimerate', \
                       'log_stoprate log_crimerate', 'log_crimerate log_population', 'log_crimerate policy'], axis = 1)
lr12 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(x), hasconst=True) 
rslt12 = lr12.fit()
print('\nModel 12: Model 9 with year interactions and population dropped')
print(rslt12.summary())
# Model 13: Model 9 with year interactions, population, and crime rate interactions dropped
x = X_train_poly.drop(['log_stoprate year', 'log_crimerate year', 'log_population year', 'year policy', 'log_population', \
                       'log_stoprate log_population', 'log_crimerate log_population', 'log_population policy', \
                       'log_stoprate log_crimerate', 'log_crimerate policy'], axis = 1)
lr13 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(x), hasconst=True) 
rslt13 = lr13.fit()
print('\nModel 13: Model 9 with year and crime rate interactions as well as population dropped')
print(rslt13.summary())
# Test model 13 for multicollinearity
vif = [variance_inflation_factor(x.values, i) for i in range(x.values.shape[1])]
print('\nModel 13: Multicollinearity test')
print(list(zip(x.columns, vif)))
# Model 14: Model 9 with year, year interactions, population, and crime rate interactions dropped
x = X_train_poly.drop(['log_stoprate year', 'log_crimerate year', 'log_population year', 'year policy', 'log_population', \
                       'log_stoprate log_population', 'log_crimerate log_population', 'log_population policy', \
                       'log_stoprate log_crimerate', 'log_crimerate policy', 'year'], axis = 1)
lr14 = sm.OLS(y_train[['log_nonstop_arrestrate']].reset_index(drop = True), sm.add_constant(x), hasconst=True) 
rslt14 = lr14.fit()
print('\nModel 14: Model 9 with year, year and crime rate interactions as well as population dropped')
print(rslt14.summary())
# Test model 14 for multicollinearity
vif = [variance_inflation_factor(x.values, i) for i in range(x.values.shape[1])]
print('\nModel 14: Multicollinearity test')
print(list(zip(x.columns, vif))) 
# Test model 5 for multicollinearity
vif = [variance_inflation_factor(X_train[['log_stoprate','log_crimerate']].values, i) \
       for i in range(X_train[['log_stoprate','log_crimerate']].values.shape[1])]
print('\nModel 5: Multicollinearity test')
print(list(zip(['log_stoprate','log_crimerate'], vif))) 