#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:15:23 2019
The following is to understand if the police stop-question-frisk policy
has an effect on crime.
We use the NYC offense, arrest, and stop-question-frisk data, aggregated 
annually and at the precinct level.  
@author: Brad & Anil
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import seaborn as sns
df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/df.csv')
df = df.dropna()
df = df.drop(df.loc[(df.YEAR < 2008) | (df.YEAR == 2013)].index)
df['policy_change'] = [1 if year > 2013 else 0 for year in df.YEAR ]
df['crime_rate'] = 1000 * df.CMPLNTS / df.POPULATION
df['nonsqf_arrests'] = df.ARRESTS - df.STOP_ARRESTS
df['nonsqf_arrest_rate'] = 1000 * df.nonsqf_arrests / df.POPULATION
df['arrest_rate'] = 1000* df.ARRESTS / df.POPULATION
df['sqf_arrest_rate'] = 1000 * df.STOP_ARRESTS / df.POPULATION
df['stop_rate'] = 1000 * df.STOPS / df.POPULATION
# Relationship between stop rates and crime rates across precincts and time
ax1 = sns.scatterplot(x = 'stop_rate', y = 'crime_rate', hue = 'policy_change', data = df)
ax1.set_ylim(0,175)
ax1.set_xlim(0,350)
ax1.set_xlabel('Stops per 1,000 population')
ax1.set_ylabel('Reported offenses per 1,000 population')
ax1.set_title('Stop Rate and Crime Rate Vary over Time and across Precints')
ax1.legend()
# Relationship between arrest rates and crime rates across precincts and time
ax1 = sns.scatterplot(x = 'nonsqf_arrest_rate', y = 'crime_rate', data = df)
ax1.set_ylim(0,175)
ax1.set_xlim(0,200)
ax1.set_xlabel('Arrests per 1,000 population')
ax1.set_ylabel('Reported offenses per 1,000 population')
ax1.set_title('Crime and Arrest Rates are Highly Correlated across Time and across Precints')
# Construct X and y matrices for model fitting
feats = ['POPULATION', 'ARRESTS', 'nonsqf_arrests', 'nonsqf_arrest_rate',\
         'stop_rate','YEAR','policy_change', 'ADDR_PCT_CD']
X = df[feats].values
y = df[['CMPLNTS','crime_rate']].values
# Split the data into test and training samples--stratify by year
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = X[:,5], \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
# Model 1: absolute values - basic - only population
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 2: absolute values - basic with arrests
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0:2]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 3: absolute values - basic with nonstop arrests
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0:3]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 4: switch to rates - basic with nonstop arrests
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# For model 4 calculate residuals
res = y_train[:,1]-rslt.predict(sm.add_constant(X_train[:,3]))
ax1 = sns.scatterplot(x = X_train[:,4], y = res, hue = X_train[:,6])
ax1.set_ylim(-75,75)
ax1.set_xlim(0,350)
ax1.set_xlabel('Stops per 1,000 population')
ax1.set_ylabel('Reported offenses per 1,000 population\nafter controlling for arrest rate')
ax1.set_title('The Relationship Bewteen Stop Rate and Crime Rate is Less Obvious')
ax1.legend()
# Model 5: rates - stop rate with nonstop arrests
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3:5]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 6: rates - stop rate with nonstop arrests and time trend
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3:6]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 6: rates - stop rate with nonstop arrests and policy change - poly features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
lr = sm.OLS(y_train[:,1], poly.fit_transform(X_train[:,3:7]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Test model 6 for collinearity
from statsmodels.stats.outliers_influence import variance_inflation_factor
X_train_poly = poly.fit_transform(X_train[:,3:7]) 
vif = [variance_inflation_factor(X_train_poly, i) for i in range(1,X_train_poly.shape[1])]
#list(zip(refined_cols, vif))
#sns.pairplot(X_train_poly)
# Model 7: rates - stop rate with nonstop arrests and policy change
interaction = X_train[:,4]*X_train[:,6]
lr = sm.OLS(y_train[:,1], np.concatenate((X_train[:,3:7],interaction.reshape(-1,1)), axis = 1), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Test model 7 for collinearity

vif = [variance_inflation_factor(np.concatenate((X_train[:,3:7],interaction.reshape(-1,1)), axis = 1), i) \
                                 for i in range(np.concatenate((X_train[:,3:7],interaction.reshape(-1,1)), axis = 1).shape[1])]