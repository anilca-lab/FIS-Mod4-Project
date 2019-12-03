#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:22:12 2019

@author: flatironschol
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
population_list = [8.0233, 7.9844, 7.9396, 7.9043, 7.9087, 7.9458, 7.9911, 8.1937, 8.2927, 8.3835, 8.4586, 8.5211, 8.5825, 8.6154, 8.6227, 8.3987]
basics_df = pd.DataFrame({'year': range(2003,2019), 'population': population_list})
offenses = ['violation-offenses', 'misdemeanor-offenses', \
            'non-seven-major-felony-offenses', 'seven-major-felony-offenses']
for offense in offenses:
    file = f'/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/{offense}-2000-2018.xls'
    df = pd.read_excel(file).T.reset_index()
    if offense == 'violation-offenses':
        df = df[[2,5]]
        df = df.rename(columns = {2: 'year', 5: offense})
    elif offense == 'misdemeanor-offenses':
        df = df[[2,20]]
        df = df.rename(columns = {2: 'year', 20: offense})
    elif offense == 'non-seven-major-felony-offenses':
        df = df[[3,12]]
        df = df.rename(columns = {3: 'year', 12: offense})
    elif offense == 'seven-major-felony-offenses':
        df = df[[3,11]]
        df = df.rename(columns = {3: 'year', 11: offense})
    df = df.drop(index = 0)
    df = df.astype('float64')
    basics_df = basics_df.merge(df, on = 'year', how = 'inner')
for offense in offenses:
    basics_df[offense] = basics_df[offense] / (10 * basics_df.population)
fig, ax1 = plt.subplots(1, 1, figsize = (6, 4))
for offense in offenses:
    sns.lineplot(x = 'year', y = offense, data = basics_df, ax = ax1, legend = 'full')
ax1.set_xticks(range(2003, 2019, 1))
ax1.set_xticklabels(range(2003, 2019, 1), rotation=90)
ax1.set_xlabel('')
ax1.set_ylim(0, 9000)
ax1.set_ylabel('Reported offenses per 100,000 population')
ax1.set_title('Declining Crime Rates in NYC')
plt.legend(offenses)
plt.show()

stops_list = [160851, 313523, 398191, 506491, 472096, 540302, 581168, 601285, 685724, 532911, 191851, 45787, 22565, 12404, 11629, 11008]
innocent_stops_list = [140442, 278933, 352348, 457163, 410936, 474387, 510742, 518849, 605328, 473644, 169252, 37744, 18353, 9394, 7833, 7645]
basics_df = basics_df.merge(pd.DataFrame({'year': range(2003, 2019), 'stops': stops_list}))
basics_df = basics_df.merge(pd.DataFrame({'year': range(2003, 2019), 'innocent_stops': innocent_stops_list}))
basics_df['stops'] = basics_df.stops / (10*basics_df.population)
basics_df['stop_arrests'] = (basics_df.stops) - (basics_df.innocent_stops / (10*basics_df.population))
fig, ax2 = plt.subplots(1, 1, figsize = (6, 4))
sns.lineplot(x = 'year', y = 'stops', data = basics_df, ax = ax2)
sns.lineplot(x = 'year', y = 'stop_arrests', data = basics_df, ax = ax2)
ax2.set_xticks(range(2003, 2019, 1))
ax2.set_xticklabels(range(2003, 2019, 1), rotation=90)
ax2.set_xlabel('')
ax2.set_ylim(0, 9000)
ax2.set_ylabel('Stops per 100,000 population')
ax2.set_title('In 2013, Stop-Question-Frisk Downsized in NYC')
plt.legend(['Stops', 'Stop arrests'])
plt.show()

population_df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/population_df.csv')
complaints_df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/complaints_df.csv')
arrests_df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/arrests_df.csv')
sqf_df = pd.read_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/sqf_df.csv')
complaints_df = complaints_df.groupby(['YEAR', 'ADDR_PCT_CD']).CMPLNTS.sum()
complaints_df = complaints_df.reset_index()
# merge complaints and population data by precinct (assume same population every year)
df = complaints_df.merge(population_df, how = 'outer',
                         left_on = 'ADDR_PCT_CD',
                         right_on = 'precinct',
                         indicator = True,
                         validate = 'many_to_one')
df = df.drop(df.loc[df.POPULATION == 0].index)
df = df.drop(['precinct', '_merge'], axis = 1)
# merge with arrests data by precinct and year
df = df.merge(arrests_df, how = 'outer',
              left_on = ['ADDR_PCT_CD', 'YEAR'],
              right_on = ['ARREST_PRECINCT', 'YEAR'],
              indicator = True,
              validate = 'one_to_one')
df = df.drop(df.loc[df.CMPLNTS.isna()].index)
df = df.drop(['ARREST_PRECINCT', '_merge'], axis = 1)
# merge with stop-and-frisk data by precinct and year
df = df.merge(sqf_df, how = 'outer',
              left_on = ['ADDR_PCT_CD', 'YEAR'],
              right_on = ['STOP_LOCATION_PRECINCT', 'YEAR2'],
              indicator = True,
              validate = 'one_to_one')
df = df.drop(df.loc[df.YEAR.isna()].index)
df = df.drop(['STOP_LOCATION_PRECINCT', 'YEAR2', '_merge'], axis = 1)

df.to_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/df.csv')
=