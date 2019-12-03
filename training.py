#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:15:23 2019

@author: flatironschol
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
stops_df = df.groupby(['ADDR_PCT_CD', 'policy_change']).mean().STOPS.reset_index()
sns.scatterplot(x = 'ADDR_PCT_CD', y = 'STOPS', hue = 'policy_change', data = stops_df)

df['crime_rate'] = 1000 * df.CMPLNTS / df.POPULATION
df['nonsqf_arrest_rate'] = 1000 * (df.ARRESTS - df.STOP_ARRESTS) / df.POPULATION
df['arrest_rate'] = 1000* df.ARRESTS / df.POPULATION
df['sqf_arrest_rate'] = 1000 * df.STOP_ARRESTS / df.POPULATION
df['stop_rate'] = 1000 * df.STOPS / df.POPULATION

df['year'] = df.YEAR - 2007


stop_rate_df = df.groupby(['policy_change', 'ADDR_PCT_CD']).stop_rate.mean()
stop_rate_df = stop_rate_df.unstack(level = 0).reset_index()
stop_rate_df.columns = ['precinct', 'pre2013_stop_rate', 'post2013_stop_rate']
crime_rate_df = df.groupby(['policy_change', 'ADDR_PCT_CD']).crime_rate.mean()
crime_rate_df = crime_rate_df.unstack(level = 0).reset_index()
crime_rate_df.columns = ['precinct', 'pre2013_crime_rate', 'post2013_crime_rate']
crime_vs_stops_df = crime_rate_df.merge(stop_rate_df, on = 'precinct')
crime_vs_stops_df['d_stop_rate'] = crime_vs_stops_df.post2013_stop_rate - crime_vs_stops_df.pre2013_stop_rate
ax1 = sns.scatterplot(x = 'pre2013_crime_rate', y = 'd_stop_rate', data = crime_vs_stops_df)
ax1.set_ylim(-200, 0)
ax1.set_xlim(20, 100)
ax1 = sns.scatterplot(x = 'pre2013_crime_rate', y = 'post2013_crime_rate', data = crime_vs_stops_df)
ax1.set_ylim(20, 100)
ax1.set_xlim(20, 100)
crime_vs_stops_df['d_crime_rate'] = crime_vs_stops_df.post2013_crime_rate - crime_vs_stops_df.pre2013_crime_rate
ax1 = sns.scatterplot(x = 'd_crime_rate', y = 'd_stop_rate', data = crime_vs_stops_df)
ax1.set_ylim(-200, 0)
ax1.set_xlim(-20, 20)
arrest_rate_df = df.groupby(['policy_change', 'ADDR_PCT_CD']).arrest_rate.mean()
arrest_rate_df = arrest_rate_df.unstack(level = 0).reset_index()
arrest_rate_df.columns = ['precinct', 'pre2013_arrest_rate', 'post2013_arrest_rate']
ax1 = sns.scatterplot(x = 'pre2013_arrest_rate', y = 'post2013_arrest_rate', data = arrest_rate_df)
ax1.set_ylim(0, 100)
ax1.set_xlim(0, 100)

# Model 1: absolute values
X = df[['STOPS', 'POPULATION', 'year']].values
y = df.CMPLNTS.values
X = sm.add_constant(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = df.year.values, \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
lr = sm.OLS(y_train, X_train)
rslt = lr.fit()
rslt.summary()

# Model 2: absolute values with arrests
X = df[['STOPS', 'POPULATION', 'year', 'ARRESTS']].values
y = df.CMPLNTS.values
X = sm.add_constant(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = df.year.values, \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
lr = sm.OLS(y_train, X_train)
rslt = lr.fit()
rslt.summary()

# Model 3: rates
df['arrest_rate'] = 1000 * df.ARRESTS / df.POPULATION
X = df[['stop_rate', 'year', 'arrest_rate']].values
y = df.crime_rate.values
X = sm.add_constant(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = df.year.values, \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
lr = sm.OLS(y_train, X_train)
rslt = lr.fit()
rslt.summary()

# Test model 3 for collinearity
