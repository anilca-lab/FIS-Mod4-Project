#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019
The following is a part of the FIS Mod4 Project
The project aims to examine the relationship between stop-question-frisk
and policy effectiveness using data from the NYPD.
Data were initially processed using R. The following merges the aggregated data
and engineers new features.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("talk")
sns.set_style("white")
df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/df.csv')
# Construct X and y matrices for model fitting
feats = ['POPULATION', 'CMPLNTS', 'STOPS', 'crime_rate', 'stop_rate',\
         'YEAR','policy_change', 'sqf_arrest_rate', 'ADDR_PCT_CD']
X = df[feats].values
y = df[['nonsqf_arrests','nonsqf_arrest_rate','ARRESTS']].values
# Split the data into test and training samples--stratify by year
X_train, X_test, y_train, y_test = train_test_split(X, y, \
                                                    stratify = X[:,5], \
                                                    test_size = 0.2, \
                                                    random_state = 120219)
# Model 1: absolute values - basic - only population
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 2: absolute values - basic with crime
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0:2]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 3: absolute values - basic with stops and crime
lr = sm.OLS(y_train[:,0], sm.add_constant(X_train[:,0:3]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 4: switch to rates - basic with crime
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# For model 4 calculate residuals
res = y_train[:,1]-rslt.predict(sm.add_constant(X_train[:,3]))
fig, ax1 = plt.subplots(1, 1, figsize = (10, 6))
sns.scatterplot(x = X_train[:,4], y = res, hue = X_train[:,6], ax = ax1)
ax1.set_ylim(-75,75)
ax1.set_xlim(0,350)
ax1.set_xlabel('Stops per 1,000 population')
ax1.set_ylabel('Reported offenses per 1,000 population\nafter controlling for arrest rate')
ax1.set_title('The Relationship Between Stop Rate and Crime Rate is Less Obvious')
leg = ax1.get_legend()
for t, l in zip(leg.texts, ['before 2013','after 2013']): t.set_text(l)
plt.legend()
# Model 5: rates - stop rate with crime
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3:5]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 6: rates - stop rate with crime and time trend
lr = sm.OLS(y_train[:,1], sm.add_constant(X_train[:,3:6]), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 7: rates - stop rate with crime and policy change - time trend omitted
x = np.concatenate((X_train[:,3:5], X_train[:,6].reshape(-1,1)), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 8: rates - stop rate with crime and policy change interaction
interaction = X_train[:,4]*X_train[:,6]
x = np.concatenate((x, interaction.reshape(-1,1)), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Test model 8 for multicollinearity
feats8 = feats[3:5] + [feats[6]] + ['stops_policy_inter'] 
vif = [variance_inflation_factor(x, i) for i in range(x.shape[1])]
list(zip(feats8, vif))
# Model 9: rates - stop rate with crime, policy change interaction, stop arrests
x = np.concatenate((X_train[:,3:5], X_train[:,6:8]), axis = 1)
interaction1 = X_train[:,4]*X_train[:,6]
interaction2 = X_train[:,7]*X_train[:,6]
interaction = np.concatenate((interaction1.reshape(-1,1), interaction2.reshape(-1,1)), axis =1)
x = np.concatenate((x, interaction), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Test model 9 for multicollinearity
feats9 = feats[3:5] + feats[6:8] + ['stops_policy_inter', 'sqf_arrests_policy_inter'] 
vif = [variance_inflation_factor(x, i) for i in range(x.shape[1])]
list(zip(feats9, vif))
# Model 10: rates - stop rate with crime, policy change interaction, 
# stop arrests and population
x = np.concatenate((x, X_train[:,0].reshape(-1,1)), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Model 11: rates - sqf arrest rate with nonstop arrests, policy change interaction
x = np.concatenate((X_train[:,3].reshape(-1,1), X_train[:,6:8]), axis = 1)
interaction = X_train[:,6]*X_train[:,7]
x = np.concatenate((x, interaction.reshape(-1,1)), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
# Test model 11 for multicollinearity
feats11 = [feats[3]] + feats[6:8] + ['sqf_arrests_policy_inter'] 
vif = [variance_inflation_factor(x, i) for i in range(x.shape[1])]
list(zip(feats11, vif))
# Model 12: rates - stop rate with population and policy change interaction
x = np.concatenate((X_train[:,0].reshape(-1,1), X_train[:,4].reshape(-1,1)), axis = 1)
x = np.concatenate((x, X_train[:,6:8]), axis = 1)
interaction1 = X_train[:,4]*X_train[:,6]
interaction2 = X_train[:,7]*X_train[:,6]
interaction = np.concatenate((interaction1.reshape(-1,1), interaction2.reshape(-1,1)), axis =1)
x = np.concatenate((x, interaction), axis = 1)
lr = sm.OLS(y_train[:,1], sm.add_constant(x), hasconst=True)
rslt = lr.fit()
rslt.summary()
