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
# drop missing observations, outliers while limiting the period to
# 2008-12 and 2014-18
df = df.dropna()
df = df.drop(df.loc[(df.YEAR < 2008) | (df.YEAR == 2013)].index)
df = df[~df.ADDR_PCT_CD.isin([22, 14])]
# engineer new features
# scale the variables by population
# define a policy change dummy set to 1 for 2014-18 period
df['policy_change'] = [1 if year > 2013 else 0 for year in df.YEAR ]
df['crime_rate'] = 1000 * df.CMPLNTS / df.POPULATION
df['nonsqf_arrests'] = df.ARRESTS - df.STOP_ARRESTS
df['nonsqf_arrest_rate'] = 1000 * df.nonsqf_arrests / df.POPULATION
df['arrest_rate'] = 1000* df.ARRESTS / df.POPULATION
df['sqf_arrest_rate'] = 1000 * df.STOP_ARRESTS / df.POPULATION
df['stop_rate'] = 1000 * df.STOPS / df.POPULATION
# export the dataframe
df.to_csv('/Users/flatironschol/FIS-Projects/Module4/FIS-Mod4-Project/data/df.csv')
